
import numpy
import pyodbc
import sys, os
import matplotlib

import datetime

from dataRetriever import dataRetriever
from covariate import covariate
from configParser import paramConfigParser

from ml import Learner 
from mytools import *

def main():

    config_key = sys.argv[1]
    
    cparser = paramConfigParser("config.ini", config_key) 

    now = datetime.datetime.now() - datetime.timedelta(1)
    c = covariate(cparser)     
    #Dataset = c.DataSet(datetime.datetime(2013, 8, 1), datetime.datetime(2013, 8, 30))
    Dataset = c.DataSet(datetime.datetime(2013, 8, 1), datetime.datetime(now.year, now.month, now.day)) 

    '''
    dataset, label = Dataset 
    for key in sorted(dataset.keys()):
	print key + ":" + str(len(dataset[key]))
	print dataset[key]

    for key in sorted(dataset.keys()):
	print len(dataset[key])

    '''

    L = Learner(Dataset)
    L.train()


    now += datetime.timedelta(1)
    if (now.hour < 16):
	observation = c.Observation(datetime.datetime.now())
    else:
	observation = c.Observation(datetime.datetime.now() + datetime.timedelta(1))


    status = L.evaluate(observation)
    
    '''
    for t in sorted(observation.keys()):
	print observation[t]

    '''

    for key in sorted(status.keys()):
	
	print key
	
	print status[key]

    commit(status, config_key)

    #fanStatusMatrix = c.fanStatusMatrix()

def commit(status, config_key):

    offset = []
    for key in sorted(status.keys()):
	
	l = status[key]

	indeces = range(0, len(status[key]))
	indeces.reverse()

	for i in indeces:
	    if status[key][i] == 1:
		print str(i/4) + ":" + str((i%4)*15)
		offset.append(i*15)
		break

    rdt = numpy.average(offset)
    print "rampdown time is" + str(rdt/60) + ":" + str(rdt%60)

    minrdt = numpy.min(offset)

    if config_key == "345_Park":
	rdt = minrdt 

    now = datetime.datetime.now()
    run_datetime = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    date = datetime.datetime.now()
    if now.hour > 16:
	date += datetime.timedelta(1)

    ramp_down_time = datetime.datetime(date.year, date.month, date.day, int(rdt/60), int(rdt%60))

    cparser = paramConfigParser('config.ini', config_key)

    connection = connectTo(cparser.server(), cparser.database(), cparser.uid(), cparser.pwd())
    cursor = connection.cursor()

    query = "INSERT INTO " + cparser.occupancyRampdownTable() + " (Run_DateTime, Prediction_DateTime) Values ('" + str(run_datetime)[:23] + "', '" + str(ramp_down_time)[:23] + "')"

    cursor.execute(query)
    cursor.commit()

    cursor.close()
    connection.close()
main()
