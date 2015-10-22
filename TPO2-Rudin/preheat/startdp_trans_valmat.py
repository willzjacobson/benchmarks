# -*- coding: utf-8 -*-
"""
Created on Tue May  6 20:28:21 2014

@author: 4d
"""

from sklearn.ensemble import ExtraTreesRegressor as tree
import pandas as pd
import numpy as np
import datetime
import adp
import os
import pylab as plt
import seaborn as sns
from functools import partial
import pdb
from startdpPreprocess import filt_bins, comp_mns, discretize, check0
import processData
import cPickle as pickle
from sklearn.externals import joblib


def get_states(data, cols):
    '''
    generates a dict of the set of states/actions
    '''
    return {c: range(int(np.round(data[c].min())),(int(np.round(data[c].max()))+1)) for c in cols}
    

    
def build_model(df,cols,dep, ntrees = 100):
    '''
    builds our ERF regression
    '''
    print 'building %s model' % dep
    model = tree(n_estimators = ntrees)
    return model.fit(df[cols],df[dep])
    
def steam_traunches(usage):
    '''
    finds total steam cost based on total usage
    '''
    traunches = np.array([31.06, 30.22, 27.919, 26.236, 23.197])
    maxes = np.array([250, 1250, 3500, 20000, 25000]) 
    cost = np.zeros((5))
    for i in range(0,5):
        if usage > cost[i]:
            cost[i] = min(usage, maxes[i])
            usage -= maxes[i]
    return np.dot(cost, traunches)
    
def comp_fan(pumpbin, lagbin):
    '''
    finds actual startup time in number of hours since midnight
    '''
    ptime = pumpbin*.25 + 4.75
    ltime = lagbin*.25 + .25 
    return ptime + ltime

def build_peaktrans(data, cols):
    '''
    builds a dictionary of peak transitons between state/action and state
    
    inputs:
    cols - set of states/actions
    data - dataframe of input data
    
    output:
    trans - dicto of transition matrices
    '''
    trans = {}
    for c in cols:

        if c != 'peakbin':
            #generate raw counts
            mat = pd.pivot_table(data, values=data.columns[0], rows=['peakbin'], cols=[c], aggfunc=pd.DataFrame.count)
            #smoothing factor            
            consts = 1/mat.sum()
            mat = mat.fillna(consts)
        else:
            #generate raw counts
            mat = pd.pivot_table(data, values=data.columns[0], rows=['%s1' % c], cols=[c], aggfunc=pd.DataFrame.count).fillna(0)
            #smoothing factor            
            consts = 1/mat.sum()
            for k in mat.columns:
                j = int(k)
                for s in mat.index:
                    #note all transitions must not include lower states
                    if s < j and mat[k].ix[s] != 0:
                        mat[k].ix[j] += mat[k].ix[s]
                        mat[k].ix[s] = 0
                    elif (s>j) and mat[k].ix[s] == 0:
                        mat[k].ix[s] = consts[k]
        trans[c] = mat/mat.sum()
    return trans

def build_valmat(states, acts, actsdict, models, data):
    dims = [len(v) for v in states.values()]
    #print states.keys()
    dims += [data[a].max()+1 for a in acts]
    print 'size of value matrix: %s' % dims
    # THIS PART IS HARD CODED AND NEEDS TO BE MULTINDEXED LATER BECAUSE WE"RE LAME
    costs = {k: np.zeros(dims) for k in ['steamUsage', 'elecUsage','peak', 'cost']}
    temps = states['tempbin']
    supercosts = [s * 2 * 1629.92 for s in sorted(states['peakbin'])]
    for n in temps:
        #print 'temp = %f' % n
        if n <= 4:
            f = 1
        else: 
            f = 0
        for t in actsdict['pumpbin']:
            #print 'pumptime = %f ' % t
            for k in actsdict['lagbin']:
                #print 'lag time = %f' % comp_fan(t,k)
                if comp_fan(t,k) < 7:
                    #print 'valid action combination'
                    ind = [n,t,k,f]
                    for m in models.keys():
                        costs[m][n,:,t,k] = float(models[m].predict(ind))
                    usage_cost = steam_traunches(costs['steamUsage'][n,:,t,k][0])
                    elec_cost = costs['elecUsage'][n,:,t,k][0] * .077
                    peak = costs['peak'][n,:,t,k][0] *169.32
                    costs['cost'][n,:,t,k] = usage_cost + elec_cost + peak + supercosts
                    #print 'costs : %s' % str(costs['cost'][n,:,t,k]).strip('[]')
                else:
                    #print 'invalid action combination'
                    for c in costs.values():
                        c[:,:,t,k] = np.nan
    return costs

def prep_ext_data(path, filters, bnvars):
    #pulls external data for pump transitions
    full = processData.load_originals(path)
    filtered = processData.flt(full, filters)
    filtered = discretize(filtered, bnvars)
    filtered = check0(filtered, bnvars)
    return filtered

def look_ahead(series):
    #finds state the following day given a state varible
    return [series.iloc[i+1] if i+1 < len(series.index) else float('NaN') for i in xrange(len(series.index))]


def get_data(path, fname):
    data = {c: pd.read_csv(os.path.join(path, '%s_%s.csv' % (fname, c)), index_col = 0, parse_dates = 0) for c in ['train','test']}
    return data

def pull_srcs(train, test, cfg):
    #pull external data and clean with original training data
    fullbns = cfg['Valmat']['fullbins'].split(' ')
    fulbnvrs = {f: cfg['BinVars'][f] for f in fullbns}
    fullflts = {f: cfg['Filters'][f] for f in cfg['Valmat']['fullfilts'].split(' ')}
    full = prep_ext_data(cfg['Valmat']['full'],fullflts, fulbnvrs)
    sts = [train, full, test]
    binnames = [c for c in fulbnvrs]
    for na in binnames:
        #making sure that maximum state in train and test sets are the same
        sts = comp_mns(sts, na)        

    return sts
    
def makefullpktrans(train, full):
    #builds full peak trans based on two datasets, returns dict of transition matrices
    peaktrans0 = build_peaktrans(train,['lagbin'])
    peaktrans1 = build_peaktrans(full,['pumpbin','peakbin'])
    peaktrans = dict(peaktrans0.items() + peaktrans1.items())
    return peaktrans


def trans_and_valmat(cfg, train, test):
    '''
    given training data and config file, builds models, peak transtions, and costs matrices
    '''
    sts = pull_srcs(train,test,cfg)
    train = check0(train, cfg['BinVars'])
    train = sts[0]
    full = sts[1]
    test = sts[2]
    full['peakbin1'] = look_ahead(full['peakbin'])
    print 'building peak transition'
    peaktrans = makefullpktrans(train, full)
    assert (sorted(test['peakbin'].unique()) == sorted(list(peaktrans['peakbin'].index))), 'peak states do not match' 
    mnames = cfg['Valmat']['models'].split(' ')
    snames = cfg['Valmat']['states'].split(' ')
    acts = cfg['Valmat']['actions'].split(' ')
    mcols = [snames[0]] + acts + ['fp']
    build = partial(build_model, df = train,cols = mcols)
    models = {n: build(dep = n) for n in mnames}
    states = get_states(train,snames)
    actsdict = get_states(train,acts)
    print 'building value matrix'
    costs = build_valmat(states, acts, actsdict, models, train)
    return peaktrans, models, costs, train, test

def writefile(path,name,subname,data):
    with open(os.path.join(path, '%s_%s.pkl' % (name, subname)),'wb') as f:
        pickle.dump(data,f)
    print 'writing %s matrix' % subname
        

if __name__ == "__main__":  
    cfg = processData.start_file()
    print 'loading training data'
    data = get_data(cfg['OutPath']['outdir'],cfg['OutPath']['outfile'])
    peaktrans, models, costs, train, test = trans_and_valmat(cfg, data['train'])
    pdb.set_trace()
    train.to_csv(os.path.join(cfg['OutPath']['outdir'],'%s_%s.csv' % (cfg['OutPath']['outfile'],'train')))
    train.to_csv(os.path.join(cfg['OutPath']['outdir'],'%s_%s.csv' % (cfg['OutPath']['outfile'],'test')))
    for k,m in models.iteritems():
        print 'writing %s model' % k
        joblib.dump(m, os.path.join(cfg['OutPath']['outdir'], '%s_%sERF.pkl' % (cfg['OutPath']['outfile'], k)))
    tofile = partial(writefile, path = cfg['OutPath']['outdir'], name = cfg['OutPath']['outfile'])
    tofile(subname = 'peaktrans', data = peaktrans)
    for c,v in costs.iteritems():
        tofile(subname = c,data = v)
    

    



