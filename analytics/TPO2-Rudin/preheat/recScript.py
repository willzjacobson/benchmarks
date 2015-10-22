# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
#import argparse
from dbInterface import dbInterface


def preheat_rec(temp, date):
    '''produces a preheat time recommendation
    @param  temp : 
    a float consisting of the predicted average temperature between that day at 7:00
    and the previous day at 17:00

    @param date:
    a python date object the date for which a prediction is requested
 
 
     @return recDateTime:
     datetime object of the recommended date and time for preheat
     '''
	
    #ADDED TO FIX
    date += datetime.timedelta(1)
    #ADDED TO FIX
	
    date = date.date()
    baseline['l1'] = pd.Series(np.absolute(baseline['avgTemp'] - temp), index = baseline.index)
    choices = baseline.sort('l1')
    choices = choices.ix[:25]
    rec = choices['preheatTime'].ix[choices['peakDemand'].argmin()]
    recTime = datetime.datetime.strptime(rec, '%H:%M')
    recTime = recTime.time()
    recDateTime = datetime.datetime.combine(date, recTime)
    return recDateTime

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description = "Batch History drawer")
    #parser.add_argument('avgTemp', type = float, help = 'Average Temperature Between 17:00 the day before and 07:00 that day in Farenheight')    
    #parser.add_argument('date', type = str, help = 'String of Date for Prediction')
    #args = parser.parse_args()

    now = datetime.datetime.now()

    if now.hour < 5:
        predictDate = now - datetime.timedelta(days = 1)
    else:
        predictDate = now 
    
    try:
        baseline = pd.read_csv('./data/recData.csv',index_col = 0, parse_dates = 0)
    except IOError:
            print 'cannot load baseline data', baseline
    
    columns = ['avgTemp', 'preheatTime', 'peakDemand']
    
    assert list(baseline.columns) == columns, 'column names do not match'
    
    assert len(baseline.index) > 0, 'baseline data must not be empty'
        
    i = dbInterface()
    
    avgTemp = i.getAverageTemperature(predictDate)
     
    rec = preheat_rec(avgTemp, predictDate)
    
    i.commitForecast(rec)

    print rec

