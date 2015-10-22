
from dataRetriever import dataRetriever
import matplotlib.pyplot as plt
import numpy
from numpy import linalg as LA

import pyodbc
import operator
import datetime
import math

from dayCluster import dayClustering
from configParser import paramConfigParser
		

def fall_back(ConfigFileName, ConfigFileKey, mode, log):

	cparser = paramConfigParser(ConfigFileName, ConfigFileKey)
	Server = cparser.server()
	DB = cparser.database()
	UID = cparser.uid()
	PWD = cparser.pwd()
	Connection = pyodbc.connect('DRIVER={SQL SERVER};SERVER='+Server+';DATABASE='+DB+';UID='+UID+';PWD='+PWD)
	
	dr = dataRetriever(Connection)
	
	tables = cparser.startupTableName()
	#tables = cparser.startupTableNameList()
	
	if not(isinstance(tables, list)):
		tables = [tables]
	else:
		tables = tables
	
	startupTable = cparser.outputStartUpTable()
	rampdownTable = cparser.outputRampDownTable()
	
	
	
	date = datetime.datetime.now() + datetime.timedelta(0, 3600*12)
	dc = dayClustering(ConfigFileName, ConfigFileKey)
	mostLikelyDays = dc.getSimilarDays(date)
	
	startup = dr.retrieve(startupTable, orderby='Prediction_DateTime', order='desc')
	rampdown = dr.retrieve(rampdownTable, orderby='Prediction_DateTime', order='desc')
	
	startup_flag = True
	rampdown_flag = True
	
	for entry in startup:
		if (entry.Prediction_DateTime.year, entry.Prediction_DateTime.month, entry.Prediction_DateTime.day) == (date.year, date.month, date.day):
			startup_flag = False
			
	for entry in rampdown:
		if (entry.Prediction_DateTime.year, entry.Prediction_DateTime.month, entry.Prediction_DateTime.day) == (date.year, date.month, date.day):
			rampdown_flag = False
	
	#print mostLikelyDays[0][1]
	
	print tables
	#log.info(str(tables)+"\n")
	
	for table in tables:
		entries = dr.retrieve(table, 'FLOOR', distinct = True)
		floorList = []
		for e in entries:
			floorList.append(e.FLOOR)
		floorList.sort()
			#print floorList
	
		startUpTime = []
		rampDownTime = []
	
		prob = []
		for i in range(0, 20):
			prob.append(1/mostLikelyDays[i][0])
		
		sum = 0;
	
		for i in prob:
			sum += i
		for i in range(0, len(prob)):
			prob[i] /= sum
		
		print prob
		#log.info(str(prob)+"\n")
	
		for i in range(0, 20):
		
			day = mostLikelyDays[i][1]
			nextday = str(day)
			nextday = nextday.replace('-', ' , ')
			
			nextday = list(nextday)
			charpointer = 0
			while charpointer < len(nextday):
				if charpointer == 0:
					if nextday[charpointer] == '0':
						nextday.pop(charpointer)
					else:
						charpointer += 1
				elif nextday[charpointer] == '0' and nextday[charpointer-1] == ' ':
					nextday.pop(charpointer)
				else:
					charpointer += 1
			nextday = ''.join(nextday)
			
			print nextday
			#log.info(str(nextday)+"\n")
			exec('nextday = (' + nextday + ')')
			nextday = (int(nextday[0]), int(nextday[1]), int(nextday[2]))
			exec('nextday = datetime.datetime' + str(nextday))
			nextday = nextday + datetime.timedelta(1)
			print nextday
			#log.info(str(nextday)+"\n")
		
			S = 0;
			R = 0;
			scount = 0;
			rcount = 0;
		
			for floor in floorList:
				entries = dr.retrieve(table, constraints={'TIMESTAMP': (str(day), str(nextday)), 'FLOOR': floor}, orderby='TIMESTAMP')
		
				previous = 0
				for e in entries:
					su = False
					rd = False
					if not(su) and e.VALUE - previous > 0:
						S += convert(e.TIMESTAMP)
						scount += 1
						su = True
					elif not(rd) and e.VALUE - previous < 0:
						R += convert(e.TIMESTAMP)
						rcount += 1
						rd = True
					previous = e.VALUE
			if scount != 0:
				startUpTime.append((S/scount, prob[i]))
			if rcount != 0:
				rampDownTime.append((R/rcount, prob[i]))
	
		finalStartupTime = 0
		
		normalization = 0
		for pair in startUpTime:
			if pair[0] < 480:
				finalStartupTime = finalStartupTime + pair[0]*pair[1]
				normalization += pair[1]
		if normalization > 0:
			finalStartupTime /= normalization
		else:
			finalStartupTime = 465
		
		finalRampDownTime = 0
		for pair in rampDownTime:
			finalRampDownTime = finalRampDownTime + pair[0]*pair[1]
		
		#print convert(finalStartupTime)
		#print convert(finalRampDownTime)
		
		s = convert(finalStartupTime)
		if s[0] < 6:
			h = 6
			m = 30 + int(numpy.random.rand() * 15)
			s = datetime.datetime(date.year, date.month, date.day, h, m)
		elif s[0] >= int(cparser.openHour()):
			h = int(cparser.openHour()) - 1
			m = 45 + int(numpy.random.rand() * 15)
			s = datetime.datetime(date.year, date.month, date.day, h, m)
		else:
			s = datetime.datetime(date.year, date.month, date.day, s[0], s[1])

		r = convert(finalRampDownTime)

		if r[0] < 16:
			h = 16
			m = int(numpy.random.rand() * 15)
			r = datetime.datetime(date.year, date.month, date.day, h, m)
		elif r[0] >16:
			h = 16
			m = 45 + int(numpy.random.rand() * 15)
			r = datetime.datetime(date.year, date.month, date.day, h, m)
		else:
			r = datetime.datetime(date.year, date.month, date.day, r[0], r[1])
		
		print s
		#log.info(str(s)+"\n")
		print r
		#log.info(str(r)+"\n")
		
		_hour = datetime.datetime.now().hour
		_minute = datetime.datetime.now().minute
		
		run_datetime = datetime.datetime(date.year, date.month, date.day, 12, _hour, _minute)
		run_datetime = run_datetime - datetime.timedelta(1)
		output_startup_table = cparser.outputStartUpTable()
		query1 = "INSERT INTO " + output_startup_table + " (Run_DateTime, Prediction_DateTime) VALUES " + "('" + str(run_datetime)[:23] + "', '" + str(s)[:23] + "' )"
		#print query1
		##log.write(str(query1)+"\n")
		
		output_rampdown_table = cparser.outputRampDownTable()
		query2 = "INSERT INTO " + output_rampdown_table + " (Run_DateTime, Prediction_DateTime) VALUES " + "('" + str(run_datetime)[:23] + "', '" + str(r)[:23] + "')"
		#print query2
		##log.write(str(query2)+"\n")
		
		cursor = Connection.cursor()
		
		try:
			if (mode == 'startup' and datetime.datetime.now() < s):
				print "Committing startup time for " + str(ConfigFileKey)
				#log.info(str("Committing startup time for " + str(ConfigFileKey))+"\n")
				cursor.execute(query1)
				cursor.commit()
				#continue
				
			elif (mode == 'rampdown' and datetime.datetime.now() < r):
				print "Committing rampdown time for " + str(ConfigFileKey)
				#log.info(str("Committing rampdown time for " + str(ConfigFileKey))+"\n")
				cursor.execute(query2)
				cursor.commit()
				#continue
			else:
				print "Untimely call to failover system"
				#log.info(str("Untimely call to failover system")+"\n")
			
			print "committing successful for " + str(ConfigFileKey) + " " + str(mode)
			#log.info(str("committing successful for " + str(ConfigFileKey) + " " + str(mode))+"\n")
			
		except:
			print "committing unsuccessful for " + str(ConfigFileKey) + " " + str(mode)
			#log.critical(str("committing unsuccessful for " + str(ConfigFileKey) + " " + str(mode))+"\n")
		
		
		
		
def convert(date):
	if isinstance(date, datetime.datetime):
		return date.hour*60 + date.minute
	else:
		return (int(math.floor(date/60)), int(math.floor(date%60)))
	


