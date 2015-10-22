# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:35:22 2013

"""
from dbInterface import dbInterface

import pandas as pd
import numpy as np
import datetime as dt
import os
import sys
from sklearn.externals import joblib
from sklearn.ensemble import ExtraTreesRegressor as tree

def find_cost(usage, superPenalty, penalty):
    '''
    this takes basic info about the billing structure and finds our cost
    '''
    penalty *= 169.32
    superPenalty *= 1629.92
    cost = np.zeros((5))
    traunches = np.array([31.06, 30.22, 27.919, 26.236, 23.197])
    maxes = np.array([250, 1250, 3500, 20000, 25000]) 
    for i in range(0,5):
        if usage > cost[i]:
            cost[i] = min(usage, maxes[i])
            usage -= maxes[i]
    cost = np.dot(cost, traunches) + penalty + superPenalty
    return cost


def load_models(indir, train):
    if train:
        ntrees = 100
        data = pd.read_csv(os.path.join(indir, 'wimlTrain.csv'))
        ind = ['nightTemp','pumpTime']
        dep = ['totalUsage','superPeak','peak']
        models = []        
        for d in dep:
            model = tree(n_estimators = ntrees)
            model.fit(data[ind],data[d])
            models.append(model)
        return models[0], models[1], models[2]
    else: 
        peak = joblib.load(os.path.join(indir, 'peakERF.pkl'))
        superPeak = joblib.load(os.path.join(indir, 'superPeakERF.pkl'))
        usage = joblib.load(os.path.join(indir, 'usageERF.pkl'))
    return usage, superPeak, peak 

def adp_rectime(temp, times, usage, superPeak, peak, oldUsage, oldSuper, oldPeak):
    '''
    this is the meat of the rec.
    temp: temperature
    times: possible times to consider
    usage, superPeak, peak : models for different aspects of bill structure
    oldUsage, oldSuper, oldPeak : statistics based on current steam usage to date
    
    returns time to turn on pumps along with info regarding the optimizaton
    '''    
    
    peaks = pd.Series(index = times)
    supers = pd.Series(index = times)
    predUsage = pd.Series(index = times)
    predCosts = pd.Series(index = times)
    labor = (5.75 - times) * 150
    labor[labor < 0] = 0
    laborS = pd.Series(labor, index = times)
    for i in times:
        predUsage.ix[i] = usage.predict([temp, i]) + oldUsage
        supers.ix[i] = max(superPeak.predict([temp, i]), oldSuper)
        peaks.ix[i] = max(peak.predict([temp,i]), oldPeak)
        predCosts.ix[i] = find_cost(predUsage.ix[i], supers.ix[i], peaks.ix[i])
    predCosts += laborS
    timeOpt = predCosts.idxmin()
    superOpt = supers.ix[timeOpt]
    peakOpt = peaks.ix[timeOpt]
    useOpt = predUsage.ix[timeOpt]
    return timeOpt, useOpt, superOpt, peakOpt 

def calc_usage_stats(steam):
    '''
    takes a data frame and finds what we need to know about the billing cycle:

    max demand
    total usage
    max demand between 6 and 11 on business days

    '''
    holidays = ['2011-01-01', '2011-01-06', '2011-12-25', '2012-01-01', '2012-12-25', '2013-01-01', '2013-01-21', '2013-01-27', '2013-02-18', '2013-03-29']
    days = np.array(steam.index, dtype = 'datetime64[D]')
    valid_days = np.is_busday(days, holidays = holidays)
    usage = float(steam.sum()/4.0)
    peak = float(steam.max())
    times = list(steam.index.to_pydatetime())
    hr = [x.hour > 6 and x.hour < 11 for x in times]
    superPeak = float(steam[np.logical_and(hr,valid_days)].max())
    return usage, superPeak, peak 

def genBillingList():
    billing_list = []
    billing_list.append(pd.date_range('9/24/2013', '10/22/2013'))
    billing_list.append(pd.date_range('10/23/2013', '11/20/2013'))
    billing_list.append(pd.date_range('11/21/2013', '12/23/2013'))
    billing_list.append(pd.date_range('12/24/2013', '1/24/2014'))
    billing_list.append(pd.date_range('1/25/2014', '2/21/2014'))
    billing_list.append(pd.date_range('2/22/2014', '3/25/2014'))
    return billing_list

def find_start_cycle(date, billing_list):
    for date_rng in billing_list:
        if date in date_rng:
            return date_rng[0]
    return -1


def main():
    now = dt.datetime.now()
    if now.hour < 7:
        predictDate = now
    else:
        predictDate = now + dt.timedelta(days = 1)

    argv = sys.argv
    if len(argv) != 4:
        print "Imporper use of the script."
        print "adp.py (building) (config file) (saved model)"
        return

    configFile = argv[2]
    configKey = argv[1]
    savedModel = argv[3]
    db = dbInterface(configKey, configFile)
    
    #the average temperature function references the day before the prediction date
    tempDate = predictDate - dt.timedelta(days = 1)
    avgTemp = db.getAverageTemperature(tempDate)
    #if avgTemp < db.threshold():
#	    print 'temperature below freeze protection threshold: run building overnight'
#	    return
    billing_list = genBillingList()
    start_of_cycle = find_start_cycle(predictDate.date(), billing_list)
    steam = db.getCurrentSteamSeries(start_of_cycle, now)
    steam = pd.DataFrame(steam.values(), columns=['steam'], index=steam.keys())
    steam.sort(inplace=True)

    #we load the models
    usage, superPeak, peak = load_models(savedModel, train = False)

    #we get our steam stats
    oldUsage, oldSuper, oldPeak  = calc_usage_stats(steam)    

    #these are the times we consider
    times = np.arange(3,7,.25)

    #we get our recommendation
    recTime = adp_rectime(avgTemp, times, usage, superPeak, peak, oldUsage, oldSuper, oldPeak)[0]
    
    #we format our recommendation for committing to the db
    hr = int(recTime)
    mn = int((recTime - hr) * 60)
    rec = dt.datetime.combine(predictDate, dt.time(hr,mn)) 
    print rec

    db.commitForecast(rec)


if __name__ == "__main__":
    main()

    
    
    
    
        
