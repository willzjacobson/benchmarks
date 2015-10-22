
from dataRetriever import dataRetriever
import matplotlib.pyplot as plt
import numpy
from numpy import linalg as LA

import pyodbc
import operator
import datetime
import math

from configParser import paramConfigParser

class dayClustering:

	def __init__(self, ConfigFileName, ConfigFileKey):
	
		self.cparser = paramConfigParser(ConfigFileName, ConfigFileKey)
		self.Connection = None
		
		self.weather()
	
	def connect(self, database):
		if not(self.Connection == None):
			self.Connection.close()
		self.Server = self.cparser.server()
		self.DB = database
		self.UID = self.cparser.uid()
		self.PWD = self.cparser.pwd()
		self.Connection = pyodbc.connect('DRIVER={SQL SERVER};SERVER='+self.Server+';DATABASE='+self.DB+';UID='+self.UID+';PWD='+self.PWD)
		
		self.DataRetriever = dataRetriever(self.Connection)
		
	
	def weather(self):
	
		weatherdb = self.cparser.weatherDB()
		self.connect(weatherdb)
		
		forecastTable = self.cparser.weatherHourTableName()
		
		entries = self.DataRetriever.retrieve(forecastTable, orderby = 'Date')
		
		self.Weather = {}
		
		for entry in entries:
			
			date = entry.Date[0:10]
			hour = int(entry.Date[11:13])
			minute =  int(entry.Date[14:16])
			
			timeOffset = 60*hour + minute
			
			try:
				self.Weather[date][timeOffset] = [entry.TempA, entry.TempM, entry.DewA, entry.DewM, entry.Sky, entry.WSpeedA, entry.WSpeedM, entry.WDir, entry.Humidity, entry.FeelsLikeA, entry.FeelsLikeM, entry.MSLPA, entry.MSLPM]
			except:
				self.Weather[date] = {}
				self.Weather[date][timeOffset] = [entry.TempA, entry.TempM, entry.DewA, entry.DewM, entry.Sky, entry.WSpeedA, entry.WSpeedM, entry.WDir, entry.Humidity, entry.FeelsLikeA, entry.FeelsLikeM, entry.MSLPA, entry.MSLPM]
		
	
	def similarDays(self, day):
		
		
		forecastTable = '[Hourly_Forecast]'
		entries = self.DataRetriever.retrieve(forecastTable, constraints = {'Date': day})
		
		weatherVector = {}
		
		for entry in entries:
			hour = int(entry.Date[11:13])
			minute =  int(entry.Date[14:16])
			timeOffset = 60*hour + minute
			weatherVector[timeOffset] = [entry.TempA, entry.TempM, entry.DewA, entry.DewM, entry.Sky, entry.WSpeedA, entry.WSpeedM, entry.WDir, entry.Humidity, entry.FeelsLikeA, entry.FeelsLikeM, entry.MSLPA, entry.MSLPM]
		
		
		
		#print weatherVector
		
		self.SimilarDays = {}
		for day in self.Weather:
			dif = self.compare(self.Weather[day], weatherVector)
			self.SimilarDays[day] = dif
	
	def compare(self, day1, day2):
		
		times = sorted(day1.keys())
		
		times2 = sorted(day2.keys())
		
		dif = 0
		closestIndex = 0
		
		effectiveDim = 0
		for time in times:
			try:
				dif += LA.norm(numpy.array(day1[time]) - numpy.array(day2[time]))
				#dif += self.difference(day1[time], day2[time])
				effectiveDim += 1
			except:
				while(time > times2[closestIndex]):
					closestIndex += 1
				day2attime = numpy.array(day2[times2[closestIndex-1]]) + (times2[closestIndex] - times2[closestIndex-1]) * ( numpy.array(day2[times2[closestIndex]]) - numpy.array(day2[times2[closestIndex-1]]) )
				dif += LA.norm(numpy.array(day1[time]) - day2attime)
				[closestIndex]
				effectiveDim += 1
				
		dif /= effectiveDim
		
		return dif
	
	def difference(self, vec1, vec2):
		
		n = len(vec1)
		
		effectiveDim = n
		difVector = []
		
		for i in range(0, n):
			if vec1[i] == -9999 or vec2[i] == -9999:
				effectiveDim -= 1
				difVector.append(0)
				continue
			else:
				difVector.append(vec1[i] - vec2[i])
				
		return (LA.norm(numpy.array(difVector))/effectiveDim)
	
	def startup(self):
		startupTable = '[560---------002BMSHVAFAN------VAL001]'
		entries = self.DataRetriever.retrieve(startupTable, columns = 'FLOOR', distinct = True)
		
		floorList = []
		
		for entry in entries:
			floorList.append(entry.FLOOR)
			
		X = []
			
		for floor in floorList:
			#print floor
			entries = self.DataRetriever.retrieve(startupTable, constraints = {'TIMESTAMP': ('2013-05-01', '2013-05-07')}, orderby='TIMESTAMP')
			
			t = []
			y = []
			
			for entry in entries:
				t.append(entry.TIMESTAMP)
				y.append(entry.VALUE)
			
			X.append([t, y])
		
		#figure = plt.figure()
		#ax = figure.add_subplot(111)
		#for x in X:
		#	ax.plot(x[0], x[1], 'k-', color = numpy.random.rand(3,1))
			
		#plt.show()
		
	def getSimilarDays(self, date):
		str(date)
		
		self.similarDays((str(date)[0:10], str(date + datetime.timedelta(1))[0:10]))
		
		self.SimilarDaysPairs = []
		for i in self.SimilarDays:
			self.SimilarDaysPairs.append((self.SimilarDays[i], i))
		self.SimilarDaysPairs.sort()
		
		return self.SimilarDaysPairs
		

#l = cd.getSimilarDays(datetime.datetime.now())
#for i in l:
#	print i