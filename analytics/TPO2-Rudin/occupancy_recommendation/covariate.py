
import pyodbc
import numpy
import os, sys 

from configParser import paramConfigParser
from dataRetriever import dataRetriever
from mytools import *

import datetime


class covariate:
    
    
    def __init__(self, ConfigParser):

	self.ConfigParser = ConfigParser
	#self.DataSet = {}


    def DataSet(self, beginDate, endDate):
	
	self.DataSet = {}

	connection = connectTo(self.ConfigParser.server(), self.ConfigParser.database(), self.ConfigParser.uid(), self.ConfigParser.pwd())
	
	reader = dataRetriever(connection)

	Floors = self.ConfigParser.floors()
	Quadrants = self.ConfigParser.quadrants()
	#print Floors
	#print Quadrants
	
	#keeps track of the features
	self.featureCount = 0

	#Building the skeleton for the dataset	
	interval = (str(beginDate)[:10], str(endDate)[:10]) 

	AllTimeStamps = datetimeInterval(beginDate, endDate, datetime.timedelta(0, 60*15))
	for timestamp in AllTimeStamps:
	    self.DataSet[str(timestamp)[:16]] = [timestamp.weekday()]
	    self.DataSet[str(timestamp)[:16]].append(timestamp.hour*60 + timestamp.minute)

	print "quadrants:" + str(Quadrants)
	print Floors

	self.featureCount += 2 
	for i in range(0, len(Floors)): 

	    if Quadrants == ['']:
		SpaceTempPoints = reader.retrieve(self.ConfigParser.sptTableName(), columns=["TIMESTAMP", "VALUE"], constraints = {"TIMESTAMP":interval, "FLOOR":Floors[i]}, orderby="TIMESTAMP")
	    else: 
		SpaceTempPoints = reader.retrieve(self.ConfigParser.sptTableName(), columns=["TIMESTAMP", "VALUE"], constraints = {"TIMESTAMP":interval, "FLOOR":Floors[i], "QUADRANT":Quadrants[i]}, orderby="TIMESTAMP") 
	    #print len(SpaceTempPoints) 
	    for point in SpaceTempPoints:

		timestamp = str(point.TIMESTAMP)[:16]
	
		try:
 
		    if len(self.DataSet[timestamp]) == self.featureCount:
			self.DataSet[timestamp].append(point.VALUE)
		    elif len(self.DataSet[timestamp]) < self.featureCount:
			while len(self.DataSet[timestamp]) < self.featureCount:
			    self.DataSet[timestamp].append(0) 
			    #self.DataSet[timestamp].append(None)
			self.DataSet[timestamp].append(point.VALUE)
		
		except:
		    self.DataSet[timestamp]
		    print "Unconventional timestamp for " + self.ConfigParser.sptTableName()
		    print timestamp
	
	    self.featureCount += 1

	
	dataPoints = reader.retrieve(self.ConfigParser.occupancyTable(), columns=["Prediction_DateTime", "Prediction_Value"], constraints={"Prediction_DateTime": interval}, orderby="Run_DateTime", order='desc')
	
	for datapoint in dataPoints:
	    timestamp = str(datapoint.Prediction_DateTime)[:16]

	    if len(self.DataSet[timestamp]) == self.featureCount:
		self.DataSet[timestamp].append( datapoint.Prediction_Value)

	self.featureCount += 1

	###
	### Producing Labels
	
	tables = self.ConfigParser.startupTableNameList()

	equipment = {}
	for table in tables:
	    equipment[table] = []
	    dataPoints = reader.retrieve(table, columns=["ZONE", "FLOOR", "QUADRANT", "EQUIPMENT_NO"], distinct=True)
	    for point in dataPoints:
		TUPLE = (str(point.ZONE), str(point.FLOOR), str(point.QUADRANT), str(point.EQUIPMENT_NO))
		equipment[table].append(TUPLE)

	self.Status = {}

	print equipment

	for table in tables:
	    for equip in equipment[table]:

		ZONE, FLOOR, QUADRANT, EQUIPMENT_NO = equip

		dataPoints = reader.retrieve(table, columns=["TIMESTAMP", "VALUE"], constraints={"TIMESTAMP": interval, "ZONE": ZONE, "FLOOR": FLOOR, "QUADRANT": QUADRANT, "EQUIPMENT_NO":EQUIPMENT_NO}, orderby="TIMESTAMP")

		observation = {}
		for point in dataPoints:
		    timestamp = point.TIMESTAMP 
		    observation[timestamp] = point.VALUE

		adjusted_observation = interpolateTimeseries(observation, AllTimeStamps, degree=0)

		self.Status[(table, equip)] = {}

		for t in adjusted_observation:
		    self.Status[(table, equip)][str(t)[:16]] = adjusted_observation[t]
	'''	
	for key in self.Status:
	    print key
	    for timestamp in sorted(self.Status[key]):
		print self.Status[key][timestamp]
	'''

	connection.close()
	
	connection = connectTo(self.ConfigParser.server(), self.ConfigParser.weatherDatabase(), self.ConfigParser.uid(), self.ConfigParser.pwd())

	reader = dataRetriever(connection)

	dataPoints = reader.retrieve(self.ConfigParser.weatherObservation(), columns=["Date", "TempA", "DewPointA", "Humidity", "WindSpeedA", "WindDir", "VisibilityA"], constraints={"Date":interval}, orderby="Date")

	observation = {}
	for point in dataPoints:
	    timestamp = strptime(str(point.Date)[:19], "%Y-%m-%d %H:%M:%S") 
	    try:
		observation[timestamp] = [point.TempA, point.DewPointA, point.Humidity, point.WindSpeedA, point.WindDir]
	    except:
		continue
	connection.close()

	adjustedObservation = interpolateTimeseries(observation, AllTimeStamps) 

	#print len(adjustedObservation)
	for timestamp in sorted(adjustedObservation.keys()):
		self.DataSet[str(timestamp)[:16]] += adjustedObservation[timestamp]
	
	self.featureCount += 5

	self.arrangeDataSet()

	return self.DataSet, self.Status

    def arrangeDataSet(self):
    
	corrupted_timestamp = []

	for t in self.DataSet:
	    if len(self.DataSet[t]) != self.featureCount:
		corrupted_timestamp.append(t)

	for t in corrupted_timestamp:
	    self.DataSet.pop(t)




    def Observation(self, _datetime):
	
	self.DataSet = {}

	connection = connectTo(self.ConfigParser.server(), self.ConfigParser.database(), self.ConfigParser.uid(), self.ConfigParser.pwd())
	
	reader = dataRetriever(connection)

	Floors = self.ConfigParser.floors()
	Quadrants = self.ConfigParser.quadrants()
	#print Floors
	#print Quadrants
	
	#keeps track of the features
	self.featureCount = 0

	#Building the skeleton for the dataset
	rundatetime = datetime.datetime(_datetime.year, _datetime.month, _datetime.day )
	beginDate, endDate = (rundatetime, rundatetime+datetime.timedelta(1))
	interval = (str(beginDate)[:23], str(endDate)[:23]) 

	AllTimeStamps = datetimeInterval(beginDate, endDate, datetime.timedelta(0, 60*15))
	for timestamp in AllTimeStamps:
	    self.DataSet[str(timestamp)[:16]] = [timestamp.weekday()]
	    self.DataSet[str(timestamp)[:16]].append(timestamp.hour*60 + timestamp.minute)

	print "quadrants:" + str(Quadrants)
	print Floors

	self.featureCount += 2 
	for i in range(0, len(Floors)): 

	    if Quadrants == ['']:
		SpaceTempPoints = reader.retrieve(self.ConfigParser.sptPredictionTableName(), columns=["Prediction_DateTime", "Prediction_Value"], constraints = {"Prediction_DateTime":interval, "Floor":Floors[i]}, orderby="Run_DateTime", order='desc')
	    else: 
		SpaceTempPoints = reader.retrieve(self.ConfigParser.sptPredictionTableName(), columns=["Prediction_DateTime", "Prediction_Value"], constraints = {"Prediction_DateTime":interval, "Floor":Floors[i], "Quadrant":Quadrants[i]}, orderby="Run_DateTime", order='desc')
	    #print len(SpaceTempPoints) 
	    for point in SpaceTempPoints:

		timestamp = str(point.Prediction_DateTime)[:16]
	
		try:
 
		    if len(self.DataSet[timestamp]) == self.featureCount:
			self.DataSet[timestamp].append(point.Prediction_Value)
		    elif len(self.DataSet[timestamp]) < self.featureCount:
			while len(self.DataSet[timestamp]) < self.featureCount:
			    self.DataSet[timestamp].append(0) 
			    #self.DataSet[timestamp].append(None)
			self.DataSet[timestamp].append(point.VALUE)
		    	
		
		except:
		    print "Unconventional timestamp for " + self.ConfigParser.sptPredictionTableName()
		    print timestamp
	
	    self.featureCount += 1

	
	dataPoints = reader.retrieve(self.ConfigParser.occupancyTable(), columns=["Prediction_DateTime", "Prediction_Value"], constraints={"Prediction_DateTime": interval}, orderby="Run_DateTime", order='desc')
	
	for datapoint in dataPoints:
	    timestamp = str(datapoint.Prediction_DateTime)[:16]

	    try:
		val = self.DataSet[timestamp]
	    except:
		continue

	    if len(self.DataSet[timestamp]) == self.featureCount:
		self.DataSet[timestamp].append( datapoint.Prediction_Value)

	self.featureCount += 1

	connection.close()	

	connection = connectTo(self.ConfigParser.server(), self.ConfigParser.weatherDatabase(), self.ConfigParser.uid(), self.ConfigParser.pwd())

	reader = dataRetriever(connection)

	dataPoints = reader.retrieve(self.ConfigParser.hourlyForecast(), columns=["Date", "TempA", "DewA", "Humidity", "WSpeedA", "WDir"], constraints={"Date":interval}, orderby="Fcst_Date", order='desc')

	observation = {}
	for point in dataPoints:
	    timestamp = strptime(str(point.Date)[:19], "%Y-%m-%d %H:%M:%S") 
	    try:
		observation[timestamp] = [point.TempA, point.DewA, point.Humidity, point.WSpeedA, point.WDir]
	    except:
		continue
	connection.close()
	#print observation
	#print adjustedObservation
	#print self.DataSet
	adjustedObservation = interpolateTimeseries(observation, AllTimeStamps)

	for timestamp in sorted(adjustedObservation.keys()):
		self.DataSet[str(timestamp)[:16]] += adjustedObservation[timestamp]
	
	self.featureCount += 5

	self.arrangeDataSet()


	for key in sorted(self.DataSet.keys()):
	    print key
	    print len(self.DataSet[key])
	
	
	return self.DataSet



    #def fanStatusMatrix():
    
	
