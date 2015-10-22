# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:44:35 2013

@author: 4d
"""
import configparser
import argparse
import numpy as np
import pandas as pd
import datetime
import os

def load_originals(path):
    #loads inidivudal datasets)
    data = pd.read_csv(path, index_col=0, parse_dates = [0])
    data = data.dropna()
    data = data.squeeze()
    return data

def make_seasons(index):
    #finds winter seasons
    season = pd.Series(index = index)    
    seasons = [['2010-11-22','2011-03-24'], ['2011-11-22','2012-03-25'], ['2012-11-26','2013-03-24'], ['2013-11-21','2014-03-25']]
    for i, s in enumerate(seasons):
        dti = pd.DatetimeIndex(start=s[0], end=s[1], freq='D')
        if len(set(dti).intersection(set(index))) > 0:
            season[s[0]:s[1]] = i          
    return season

def find_valid_days(index):
    #finds weekdays
    holidays = ['2011-01-01', '2011-01-06', '2011-12-25', '2012-01-01', '2012-12-25', '2013-01-01', '2013-01-21', '2013-01-27', '2013-02-18', '2013-03-29']
    days = np.array(index, dtype = 'datetime64[D]')
    return np.is_busday(days, holidays = holidays)

def get_dates(index):
    #finds inidividual dates from a time series date frame
    times = index.date
    times = sorted(list(set(times)))
    return times
    
def makeStr(hour, day):
    #cobines date and hour as int into a string
    fmt = '%Y-%m-%d %H'
    hour = datetime.time(hour)
    date = datetime.datetime.combine(day, hour)
    dateStr = date.strftime(fmt)
    return dateStr
    
def sampler(df, fullSet, varname, nsamples):
    '''
    samples a data frame based on the distribution of a series

    inputs:
    df - pandas series of the underlying distribution
    fullset - data frame to sample
    varname - variable in fullset to use as sample weights
    nsamples - number of samples
    
    output:
    sampled - a data frame with observations sampled according to df
    
    '''
    counts, bins = np.histogram(df, bins = 50, density = False)
    observations = fullSet[varname]
    obWeights = pd.Series(index = observations.index)
    for w in xrange(len(counts)):
        obWeights[ np.logical_and( observations > bins[w], observations < bins[w+1] ) ] = counts[w]
    obWeights = obWeights.fillna(0)
    obWeights = obWeights/float(obWeights.sum())
    sampled = np.random.choice(len(observations.index), size = nsamples, replace = True, p  = np.array(obWeights))
    sampledData = pd.DataFrame(columns = fullSet.columns, index = range(nsamples))
    for n in xrange(nsamples):
       sampledData.ix[n] = fullSet.ix[sampled[n]]
    return sampledData

def agg(fn, ser, const):
    '''
    applies a function to a series if the length of the series is greater than a constant
    else retrns NaN
    '''
    if len(ser) >= const:
        return fn(ser)
    else:
        return np.nan

def rateConvert(data):
    #function to convert Kw to Kwh and Mlb\hr to Mlb
    return sum(data)/4

def agreement(rec, act):
    #funtion to find if they took our recommendation
    return (act in rec.unique)
    
def hrfrac(s):
    # converts a time to number of hours since midnight
    return s.hour + s.minute/60.
    
def find_pumpTime(data):
    #finds the time of the heat exchanger turn on based on steam demand
   return hrfrac(data.idxmax().to_pydatetime() - datetime.timedelta(minutes = 15))
   
def pinOrder(data, ix):
    #converts a partiulcar time in a timeseries to number of hours since midnight
    return hrfrac(data.index[ix])
    
def idxmaxtofrac(data):
    #converts the argmax in the series to number of hours since midight
    return hrfrac(data.idxmax())
    
def conEdPeak(data):
    #finds the rolling 30 minute energy demand from a series of 15 minute time intervals
    return pd.rolling_mean(data,2)

def conEdVal(data):
    #finds the 30 minute demand maximum in an energy time series
    return conEdPeak(data).max()
    
def conEdIdx(data):
    #finds the time in which the conEd peak demand occured in number of hours since midnight
    return idxmaxtofrac(conEdPeak(data))

def aggVar(startTime, endTime, dates, df, fn, cutoff, rate):
    '''
    aggregates daily data  within a time frame and filters for days with few observations
    
    inputs:
    
    startTime - interger for first hour in day
    endTime - integer for last hour in day inclusive (so 4-7 inlcudes all time up to 7:59 am)
    dates - list of dates on which to aggregate data
    df - timeseries of data
    fn - aggregation function e.g., mean, max
    cutoff -minimum percent of observations present when including a day in the dataset
    rate - number of observations per hour
    
    output: 
    a series with daily data aggregated using fn with days with few observations marked NaN
    '''
    
    endStr = [makeStr(endTime, d) for d in dates]  
    
    if startTime > endTime:
        startStr = [makeStr(startTime, d - datetime.timedelta(1)) for d in dates]  
        day1 = datetime.datetime.combine(dates[0] - datetime.timedelta(1), datetime.time(startTime))
    else:
        startStr = [makeStr(startTime, d) for d in dates]
        day1 = datetime.datetime.combine(dates[0], datetime.time(startTime))
        
    day2 = datetime.datetime.combine(dates[0], datetime.time(endTime))

    nhours = (day2 - day1).seconds/(3600) + 1     
    
    const = int(np.ceil(cutoff*(nhours*rate)))
    print 'building variable using days with at least %d observations' % const
        
    series = [agg(fn, df[startStr[i]:endStr[i]], const) for i in xrange(len(dates))]
    return pd.Series(index = pd.DatetimeIndex(dates), data = series)

def gather_data(paths):
    '''
    loads data from various csvs
    
    input:
    
    paths - a dict of paths to csvs
    
    outputs:
    
    data - dict of datasets indexed by path key name
    dates - a list of common dates between the datasets
    '''
    data = {}
    dates = []
    for k,v in paths.iteritems():
        ki = k.replace('Path', '')
        print 'loading %s data' % ki
        data[ki] = load_originals(v)
        print 'finding available dates'
        new_dates = get_dates(data[ki].index)
        if dates == []:
            dates = new_dates
        else:
            dates = sorted(list(set(dates).intersection(set(new_dates))))
    return data, dates

def find_pump_fan(steam, start, fantime, date, const = 1):
    '''
    finds the turn on time in relation to the fan turn on
    fans turn on after the heat exchangers, so we use this information to find when the heat exchangers turned on
    
    inputs:
    steam - series of steam demand
    start - integer of when to start looking for heat exchanger turn on (eg 4 am)
    fantime - startup time in number of hours since midnight
    date - the date of the heat exchanger turn on
    const - minimum observations to consider before returning NaN
    
    output:
    pump time for the given date if number of observations that day is above const else NaN
    '''
    startstr = '%s %02d' % (date,start)
    if fantime < 7:
        hr = int(np.floor(fantime))
        mn = int((fantime-hr)*60)
    else:
        hr = 6
        mn = 59
    endstr = '%s %s' % (date, datetime.time(hr,mn).strftime('%H:%M'))
    return agg(find_pumpTime,steam[startstr:endstr],const)

def make_data(data, dates, var):
    '''
    creates an aggregated dataset of daily statistics based on particular variables
    
    inputs:
    data - dict of various datasets
    dates - dates for which to aggregate data
    var - dict with varible aggregation information
    
    output:
    full - dataset with aggregated daily data from various sources
    '''    
    
    print 'initializing data frame'
    full = pd.DataFrame(index = dates)
    for k,v in var.iteritems():
        print 'building %s variable' % k
        pram = eval(v)
        if 'cutoff' in pram.keys():
            cutoff = pram['cutoff']
        else:
            cutoff = 0
        if 'rate' in pram.keys():
            rate = pram['rate']
        else:
            rate = 4                  
        full[k] = aggVar(pram['start'], pram['end'], dates, data[pram['data']], pram['fn'], cutoff, rate)
        print '%s has %d missing' % (k, sum(np.isnan(full[k])))
    full = full.dropna()    
    print 'finding business days'    
    full['valid_days'] = find_valid_days(full.index)
    print 'finding winter billing seasons'
    full['winter_season'] = make_seasons(full.index.to_datetime())
    return full

def resample_split(dist, src, totalSize, split, varname):
    '''
    generates sampled train test sets
    
    inputs:
    dist - dataframe under whose distrbuition which we're sampling
    src - original data set used to draw sample obersvations for train and test set
    totalSize - number of samples to draw
    split - percent of samples in test set
    varname - variable name from which we are sampling
    
    outputs:
    train - training set of src data
    test- test set of src data 
    '''
    print 'sampling nights with weather similar to winter nights'
    dist = dist[varname]
    dist = dist.dropna()
    samples = sampler(dist, src, varname, totalSize)
    splitPt = int(round((totalSize * split)))
    print 'creating train and test sets'
    test = samples.ix[:splitPt - 1]
    train = samples.ix[splitPt:]
    return test, train
    
def run_sampler(smplr_info, full):
    '''
    similar to resample split, this function has additional functionality allowing us to filter data before sampling

    inupts:
    smplr_info - dict of sampler information including inputs for resample split and additional criteria to filter data
    full - dataset of source data
    
    output:
    train - training set based on full
    test - test set based on full
    '''
    samples = int(smplr_info['samples'])
    print 'intializing with %d samples' % samples
    proportion = float(smplr_info['proportion'])
    print 'initializing test set with %f test set' % proportion
    varname = str(smplr_info['varname'])
    print 'beginning to sample %s' % varname
    if 'fullset' in smplr_info.keys():
        dist = pd.read_csv(smplr_info['fullset'], index_col = 0, parse_dates = 0)
    else:
        dist = full
    if 'filter' in smplr_info.keys():
        dist = dist.query(smplr_info['fulfilter'])
    test, train = resample_split(dist, full[full['valid_days']], samples, proportion, varname)
    return test, train 
    
def flt(data, filt):
    '''
    filters data based on specific criteria
    
    inputs:
    data - original dataset
    filt - string with query criteria
    
    output:
    filtered data
    '''
    for f in filt.values():  
        data = data.query(f)
    return data

def start_file():
    #loads the config file
    parser = argparse.ArgumentParser(
        description=globals()['__doc__'],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-c', '--config', required=True,
        help='Path to config file')
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    cfg.optionxform = str
    print 'reading config file %s' % args.config
    cfg.read(args.config)
    return cfg

if __name__ == "__main__":
    cfg = start_file()
    #pull data
    data, dates = gather_data(cfg['InPaths'])
    #aggregate data based on desired variable information
    full = make_data(data, dates, cfg['Vars'])
    #adds boolean variables in daily dataset
    if 'Locgicals' in cfg:
        for k,v in cfg['Logicals'].iteritems():
            full[k] = full[eval(v)]
    #merge externally sourced daily data
    if 'Merge' in cfg:
        for m in cfg['Merge'].values():
            print '%d observations before merge' % len(full.index)
            full = full.join(load_originals(m), how = 'inner')
            print '%d observations after merge' % len(full.index)
    outdir = str(cfg.get('OutPath', 'outdir'))
    outfile = str(cfg.get('OutPath','outfile'))
    print 'writing full dataset'
    full.to_csv(os.path.join(outdir, '%s_full.csv' % outfile))
    
    if 'Sampler' in cfg:
        if 'Filters' in cfg:
            #runs filters on full set
            full = flt(full, cfg['Filters'])
        #samples train and test set
        train, test = run_sampler(cfg['Sampler'], full)
        print 'writing train and test sets'
        train.to_csv(os.path.join(outdir, '%s_train.csv' % outfile))
        test.to_csv(os.path.join(outdir, '%s_test.csv' % outfile))

