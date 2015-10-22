# -*- coding: utf-8 -*-
"""
Created on Mon May  5 14:00:19 2014

@author: 4d
"""

import pandas as pd
import numpy as np
import cPickle as pickle
import argparse
import os
import datetime
import processData
import configparser
import pdb

def binvar(ser, mn, bucket):
    '''
    discretizes our data into specific states/actions
    
    inputs:
    ser - series to discreties
    mn - minimum value to consider
    bucket - number of units in each discrete state/action (e.g. 5 degree temperature buckets)
    
    output:
    list of integers corresponding to discretized buckets
    '''
    ser -= mn
    ser /= float(bucket)
    return [int(np.round(s)) if s > 0 else 0 for s in ser]

def discretize(full, bnvrs):
    for b, v in bnvrs.iteritems():
        prams = eval(v)
        full[b] = binvar(full[prams['name']], prams['min'],prams['bucket'])
    return full

def pull_data(paths, aggvrs, bnvrs):
    '''
    aggregates data into daily data based on variable information and adds discretized state and action variables

    inputs:
    paths - dict of paths with data
    aggvrs - dicts of dicts with variable aggregation based on processData.aggvar inputs
    bnvrs - dict of inputs for binvar function

    outputs:
    data frame with daily aggregated data and discretized states and actions
    '''
    data, dates = processData.gather_data(paths)
    full = processData.make_data(data, dates, aggvrs)
    strdates = [d.strftime('%Y-%m-%d') for d in full.index]
    full['pumpTime'] = [processData.find_pump_fan(data['steam'].ix[i], 4, data['fan']['start'].ix[i],i) for i in strdates]
    full['start'] = data['fan']['start']
    full = full.dropna()
    full['fp'] = np.logical_and(full['nightUsage'] > 7, full['nightTemp'] < 36)
    full['lag'] = (full['start'] - full['pumpTime'])*60
    full = discretize(full, bnvrs)
    return full

def filt_bins(data, bnvar):
    '''
    cleans dataset to ensure that binned variables are continuous (e.g. no states are missing between the min state and the max state in the data)
    
    inputs:
    data - dataset to clean
    bnvar - binned variable to consider
    
    output:
    cleaned dataset
    '''
    m = int(data[bnvar].max())
    bns = sorted([int(i) for i in data[bnvar].unique()])
    cmpr = range(m+1)
    if bns != cmpr :
        difs = sorted(list(set(cmpr) - set(bns)))
        if difs[0] != 0:
            return data.query('%s < %d' % (bnvar, difs[0]))
        else:
            return data
    else:
        return data

def comp_mns(dfs, varname):
    '''
    compares maximum values in a binned variable between datasets and ensures all dataset have the same maximum value
    
    inputs:
    dfs - dict of data frames
    varname - varname to compare
    
    output:
    dict of filtered data frames
    '''
    mn = min([df[varname].max() for df in dfs])
    for i, df in enumerate(dfs):
        dfs[i] = df.query('%s <= %d' % (varname, mn)) 
    return dfs

def check0(data, binames):
    #additional cleaning of binned variables
    for na in binames:
        mn = data[na].min()
        assert (mn == 0),"Need to raise minimum value for %s in config file, minimum value is %f" % (na, mn)
        data = filt_bins(data,na)
    return data

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
    data['train'] = sts[0]
    data['test'] = sts[1]
    #writing output
    outdir = str(cfg.get('OutPath', 'outdir'))
    outfile = str(cfg.get('OutPath','outfile'))
    for d,v in data.iteritems():
        v.to_csv(os.path.join(outdir, '%s_%s.csv' % (outfile, d)))
    