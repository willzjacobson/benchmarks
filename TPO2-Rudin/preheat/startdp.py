# -*- coding: utf-8 -*-
"""
Created on Mon May  5 12:36:43 2014

@author: 4d
"""

import pandas as pd
import numpy as np
import cPickle as pickle
import processData
import copy
import os
import pdb

def comp_fan(pumpbin, lagbin):
    #calculates the possible fan turn on time in number of hours since midnight
    ptime = pumpbin*.25 + 4.75
    ltime = lagbin*.25 + .2
    return ptime + ltime
    
def dp(temptrans, peaktrans, val, ndays):
    '''
    value iteration to find policy
    
    inputs:
    temptrans - data frame of temperature transitions
    peaktrans - dict of dataframe with peak transitions
    val - value matrix
    ndays - number of days for backward induction (approximate length of the billing period)
    
    outputs:
    acts - policy of actions given the state
    recval - expected cost of each action at a given day and a given state aka Q_d(t,p)
    '''
    recval = np.zeros((ndays+1,len(temptrans.index), len(peaktrans['peakbin'].columns)))
    acts = {d:{t: {p: {} for p in peaktrans['peakbin'].columns} for t in temptrans.index} for d in range(ndays+1)}
    expval = np.zeros((len(peaktrans['pumpbin'].columns), len(peaktrans['lagbin'].columns)))
    backwards = np.arange(ndays,-1,-1)
    
    for day in backwards:
        print 'for day %d' % day
        #pdb.set_trace()
        for tmp in temptrans.index:
            #print 'day %s' % tmp
            # looping over the temperature ranges
            # selecting temperature transiton distribution
            ttrans = temptrans[str(tmp)] 
            for pk in peaktrans['peakbin'].columns:
                #print 'peak %s' % pk
                # looping over the possible peak demands
                #extracting the possible  value state matrix
                look = copy.copy(val[tmp,pk])
                #extracting peak transition distrubtion
                pktrans = np.array(peaktrans['peakbin'][pk])
                if day != backwards[0]:
                    for mp in peaktrans['pumpbin'].columns:
                        #print 'pump %s' % mp
                        #looping over possible heat exchanger turn on times
                        #selecting appropriate transition distribution
                        pumptrans = np.array(peaktrans['pumpbin'][mp])
                        for lg in peaktrans['lagbin'].columns:
                            #print 'lag: %s' % lg
                            #looping over possible fan turn ons
                            #if fan/pump combinaton infeasible, ignore
                            if np.isfinite(look[mp,lg]):
                                #selection appropriate transition distribution
                                lagtrans = np.array(peaktrans['lagbin'][lg])
                                #multiply and renormalize probabilities to form full transition distribution
                                ptrans = pktrans*pumptrans*lagtrans
                                ptrans /= ptrans.sum()
                                # take outer product to get the full transition in states
                                transmat = np.outer(ttrans,ptrans)
                                # get the expected value of the action
                                expval[mp,lg] = np.multiply(transmat, recval[(day+1)]).sum().sum()
                                look[mp,lg] += expval[mp,lg]
                #find the lowest cost from the actions
                optcost = np.nanmax(look)
                #selecting the appropraite action
                picks = np.where(look == optcost)
                choose = [picks[0][0],picks[1][0]]
                acts[day][tmp][pk] = choose
                #updating the value stat
                recval[day,tmp,pk] = optcost
    return acts, recval
    
def test():
    '''
    tests the DP with the value matrix [[1,0],[-1,0]] and the transtion matrix [[.6,1],[.4,0]] for 4 days
    '''
    temptrans = pd.DataFrame(np.ones([1]), index = ['0'], columns = ['0'])
    valmat = np.ones(([1,2,2,1]))
    valmat[0,:,:,0] = np.array([[1,0],[-1,0]])
    ptrans = {s : pd.DataFrame(np.ones([1]), index = ['0'], columns = ['0']) for s in ['peakbin','pumpbin','lagbin']}
    ptrans['pumpbin'] =  pd.DataFrame(np.array([[.6, 1], [.4 , 0]]), index = ['0','1'], columns = [0,1])
    ptrans['peakbin'] =  pd.DataFrame(np.array([[.5, .5], [.5 , .5]]), index = ['0','1'], columns = [0,1])
    days = 3
    acts, recval = dp(temptrans, ptrans, valmat, days)
    if all(recval[0,0] == np.array([3.056,2.36])):
        return 'test correctly computes actions'
    else:
        return 'test fails'
        
if __name__ == "__main__":
    cfg = processData.start_file()
    if 'Prams' in cfg:
        days = cfg.getint('Prams','days')
        print 'making policy for %d days' % days
    else:
        days = 32
    
    print 'reading temperature transition matrix'
    temptrans = pd.read_csv(cfg['Prams']['ttrans'], index_col = 0)
    temptrans /= temptrans.sum()
    
    print 'reading value state matrix'
    with open(cfg['Prams']['valmat'], 'rb') as f:
        val = pickle.load(f)
    
    #since these are costs we maximize the negative cost    
    val *= -1
        
    print 'reading peak transition dict'
    with open(cfg['Prams']['ptrans'], 'rb') as f:
        peaktrans = pickle.load(f)   
    acts, recval = dp(temptrans, peaktrans, val, days)
    print 'saving policy'
    names = ['actions','Qcosts']
    for i,r in enumerate([acts, recval]):
        with open(os.path.join(cfg['OutPath']['outdir'],'%s_%s.pkl' % (cfg['OutPath']['outfile'],names[i])), 'wb') as f:
            pickle.dump(r,f)
    