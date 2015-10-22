# -*- coding: utf-8 -*-
"""
Created on Tue May 13 23:40:52 2014

@author: 4d
"""

import os
import numpy as np
import pylab as plt
import cPickle as pickle
import pandas as pd
import pylab as plt
from scipy.stats import ttest_rel
import seaborn as sns
import processData
from startdp_trans_valmat import get_data, steam_traunches
from startdpPreprocess import comp_mns
from sklearn.externals import joblib
import pdb


def test_results(test, train, binnames, pi, models, costs, ptrans):
    '''
    evaluates policy on a held out test set - finds changes in cost components and change in cost
    
    inputs:
    test - data frame of test set
    train - data frame of training set
    binnames - names of binned variables
    pi - dict of policy recommendations
    modes - dict of regression trees
    costs - dict of arrays with values at each action
    ptrans - peak transition matrix
    
    output:
    results - data frame comparing costs before and after policy
    '''
    costinfo = get_prams()
    sts = [test, train]    
    for na in binnames:
        #making sure that maximum state in train and test sets are the same
        sts = comp_mns(sts, na)
    test = sts[0]
    assert (sorted(test['peakbin'].unique()) == sorted(list(ptrans['peakbin'].index))), 'peak states do not match' 
    #create billing periods
    test['bill'] = [np.floor(i/32.) for i in test.index]
    #create results variables
    test['recPump'] = pd.Series()
    test['recLag'] = pd.Series()
    for c in costinfo:
        cname = costinfo[c]['rec']
        test[cname] = pd.Series()
    print 'evaluating policy'
    for b in sorted(test.bill.unique()):
        print 'billing period %d' % b
        mo = test.query('bill == b')
        for i in mo.index:
            day = i - (b*32)
            if day == 0: 
                #at the beginning of the billing periods, peak demand is the same
                p = test['peakbin'].ix[i]
                test['recSuper'].ix[i] = p
            else:
                #else we draw from our peak transition to find our next peak under the policy
                p = int(test['recSuper'].ix[i])
            #temperature states are the same in the training set and under the policy
            t = int(mo['tempbin'].ix[i])
            #this is where we index the policy - this line gets us our recommendations - IMPORTANT FOR FUTURE REFERENCE:
            m, l = [int(k) for k in pi[day][t][p]] 
            test['recPump'].ix[i] = int(m) 
            test['recLag'].ix[i] = int(l)
            #now we find our costs
            supercost = (p* 2 * 1629.92)
            idx = (t,p,int(test['recPump'].ix[i]),int(test['recLag'].ix[i]))
            for c in ['electric', 'steam', 'peak','cost']:
                if c != 'cost':
                    test[costinfo[c]['rec']].ix[i] = costs[costinfo[c]['orig']][idx]
                else:
                    test[costinfo[c]['rec']].ix[i] = costs[c][idx]            
    
            peakcost = test['recPeak'].ix[i] * 169.32
            test['recCost'].ix[i] -= supercost 
            test['recCost'].ix[i] -= peakcost
            #here we sample from our peak transition to find what our peak state will be for the actions we've taken
            trans = ptrans['lagbin'][l] *  ptrans['pumpbin'][m] * ptrans['peakbin'][p]
            trans /= trans.sum()
            test['recSuper'].ix[i+1] = np.random.choice(range(len(trans)), p = np.array(trans))
    
    print 'evaluating cost savings of our policy for each billing period'
    bills = test.query('bill < 6').groupby('bill')           
    results = bills[['recSteam','recElec','recCost']].sum()
    results['steamUsage'] = bills['steamUsage'].sum()
    results['elecUsage'] = bills['elecUsage'].sum()
    results[['recSuper','recPeak','peakbin','conEdPeak','peak']]  = bills[['recSuper','recPeak','peakbin','conEdPeak','peak']].max()
    results['recCost'] += (results['recSuper'] * 1629.92 + results['recPeak'] * 169.32)    
    results['origCost'] = [steam_traunches(results['steamUsage'].ix[i]) for i in results.index]+(results['elecUsage'] * .077 + results['conEdPeak'] * 1629.92 + results['peak'] * 169.32)
    print 'average savings : %f' % (results['origCost'] - results['recCost']).mean()
    return results, test
 
def get_prams():
    '''
    dict of naming conventions for variables
    orig - original variable names
    rec - variable names for recommendations
    '''
    components = ['electric', 'steam', 'peak', 'superPeak','cost']
    orig = ['elecUsage','steamUsage', 'peak', 'conEdPeak','origCost']
    recs = ['recElec','recSteam', 'recPeak', 'recSuper', 'recCost']
    costinfo = {c: {} for c in components}   
    for i, c in enumerate(components):
        costinfo[c]['orig'] = orig[i]
        costinfo[c]['rec'] = recs[i]
    return costinfo
    
   
if __name__ == "__main__":  
    cfg = processData.start_file()
    print 'loading training data'
    outdir = cfg['OutPath']['outdir']
    name = cfg['OutPath']['outfile']
    data = get_data(outdir,name)
    mnames = ['steamUsage', 'elecUsage','peak']
    cnames = mnames + ['cost']
    adl = ['actions','peaktrans']
    otherfiles = {}
    costs = {c:{} for c in cnames}
    models = {m: joblib.load(os.path.join(outdir,'%s_%sERF.pkl' % (name, m))) for m in mnames}
    for a in adl:
        with open(os.path.join(outdir,'%s_%s.pkl' % (name, a))) as f:
            otherfiles[a] = pickle.load(f)
    for c in cnames:
        with open(os.path.join(outdir,'%s_%s.pkl' % (name, c))) as f:
            costs[c] = pickle.load(f)
    print 'calculating results'
    results, test = test_results(data['test'],data['train'],cfg['BinVars'], otherfiles['actions'],models, costs, otherfiles['peaktrans'])
    print 'writing results'
    test.to_csv(os.path.join(outdir, '%s_testresults.csv' % name))
    results.to_csv(os.path.join(outdir, '%s_results.csv' % name))
    
