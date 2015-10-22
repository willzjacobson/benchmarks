# -*- coding: utf-8 -*-
"""
Created on Wed May 14 12:09:20 2014

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
from startdp_trans_valmat import get_data, steam_traunches, trans_and_valmat
from startdpPreprocess import check0, pull_data, filt_bins, comp_mns
from sklearn.externals import joblib
from evalModel import test_results
import pdb
from startdp import dp

def simple_bin(ser, mn, bn):
    ser -= mn
    ser /= float(bn)
    return int(ser)


def rec_for_a_day(temp, steam, day, cfg, pi):
    '''
    this function is a basic version of the recommendation system
    
    inputs:
    temp - average night temp
    steam - peak steam demand for the billing period so far
    cfg - config file
    pi - policy
    
    output:
    m - binned pump time according to the config file
    l - binned number of minute between pump time and startup time accoridng to the config file
    '''
    day = int(day)
    binvars = {c:eval(cfg['BinVars'][c]) for c in ['tempbin', 'peakbin']}
    t = simple_bin(temp, binvars['tempbin']['min'], binvars['tempbin']['bucket'])
    p = simple_bin(steam, binvars['peakbin']['min'], binvars['peakbin']['bucket'])
    m, l = [int(k) for k in pi[day][int(t)][int(p)]] 
    return m, l

def test_recs(pi_path):
    '''
    this function tests the simple recommendation system, rec_for_a_day
    
    input:
    pi_path - path to a policy, a pickled dict
    
    output:
    m - binned pump time according to the config file
    l - binned number of minute between pump time and startup time accoridng to the config file
    '''
    temp = 30
    steam = 20
    day = 20
    cfg = {'BinVars': {}}
    pdb.set_trace()
    cfg['BinVars']['tempbin'] = str({'name': 'nightTemp', 'min': 25, 'bucket': 5})
    cfg['BinVars']['peakbin'] = str({'name': 'conEdPeak', 'min': 12, 'bucket': 3})
    with open(pi_path, 'rb') as f:
        pi = pickle.load(f)
    print rec_for_a_day(temp, steam, day, cfg, pi)
  
if __name__ == "__main__":  
    cfg = processData.start_file()
    data = {}
    #getting full daily dataset
    data['full'] = pull_data(cfg['InPaths'], cfg['AggVars'],cfg['BinVars'])
    #filtereing based on filter parameters
    data['filtered'] = processData.flt(data['full'], cfg['Filters'])
    binnames = [c for c in cfg['BinVars']]
    #checking minimum value in filtered data, then for missing states and actions
    data['filtered'] = check0(data['filtered'],binnames)
    #sampling train test sets
    test, train = processData.run_sampler(cfg['Sampler'], data['filtered'])
    train = check0(train,binnames)
    sts = [train,test]
    for st in sts:
        for na in binnames:
            #checking for missing states,actions in train and test sets
            st = filt_bins(st,na)
    for na in binnames:
        #making sure that maximum state in train and test sets are the same
        sts = comp_mns(sts, na)
    train = sts[0]
    test = sts[1]
    #making transitions and value matrices
    peaktrans, models, costs, train, test = trans_and_valmat(cfg, train, test)
    costs['cost'] *= -1
    temptrans = pd.read_csv(cfg['Prams']['ttrans'])
    days = cfg.getint('Prams','days')
    #doing dp
    acts, recval = dp(temptrans, peaktrans, costs['cost'], days)
    #evaluating policy
    costs['cost'] *= -1
    results, test = test_results(test,train,cfg['BinVars'], acts,models, costs, peaktrans)
    print 'writing results'
    outdir = str(cfg.get('OutPath', 'outdir'))
    outfile = str(cfg.get('OutPath','outfile'))
    test.to_csv(os.path.join(outdir, '%s_test.csv' % outfile))
    results.to_csv(os.path.join(outdir, '%s_results.csv' % outfile))
    train.to_csv(os.path.join(outdir, '%s_train.csv' % outfile))
    for m,v in models.iteritems():
        joblib.dump(v, os.path.join(outdir, '%s_%sERF.pkl' % (outfile, m)))
    with open(os.path.join(outdir, '%s_actions.pkl' % outfile), 'wb') as f:
        pickle.dump(acts, f)
    with open(os.path.join(outdir, '%s_costs.pkl' % outfile), 'wb') as f:
        pickle.dump(costs, f)
    with open(os.path.join(outdir, '%s_peaktrans.pkl' % outfile), 'wb') as f:
        pickle.dump(peaktrans, f)
    