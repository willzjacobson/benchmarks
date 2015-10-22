
import pyodbc
import sys, os
import numpy
from configParser import paramConfigParser

import datetime

class dbInterface:
    
    def __init__(self, config_key, config_file):
	
	self.cparser = paramConfigParser(config_file, config_key)

	self.server = self.cparser.server()
	self.db = self.cparser.database()
	self.uid = self.cparser.uid()
	self.pwd = self.cparser.pwd()
	self.weatherdb = self.cparser.weatherDatabase()
	self.preheatForecastTable = self.cparser.preheatForecastTable()

    def connectionString(self, server, database, uid, pwd):
	
	return "DRIVER={SQL SERVER};SERVER=" + server + ";DATABASE=" + database + ";UID=" + uid + ";PWD=" + pwd

    def getAverageTemperature(self, date):
	
	#print self.connectionString(self.server, self.weatherdb, self.uid, self.pwd)	
	try:
	    connection = pyodbc.connect(self.connectionString(self.server, self.weatherdb, self.uid, self.pwd))
	    cursor = connection.cursor()
	    
	except:
	    print "Connection to weather database failed!"
	    return -1	
	
	query = "SELECT TEMPA FROM " + self.cparser.hourlyForecast() + " WHERE DATE > '" + str(date)[0:10] + " 17:00'" + " AND DATE < '" + str(date + datetime.timedelta(1))[0:10] + " 05:00'" + " ORDER BY Fcst_date "
	#print query	
	cursor.execute(query)
	entries = cursor.fetchall()
	
	size = 0.0
	SUM = 0.0
	for entry in entries:
	    size += 1
	    SUM += entry.TEMPA

	
	cursor.close()
	connection.close()

	return SUM/size

    def threshold(self):
	return self.cparser.freezeProtectionThreshold()

    def getCurrentSteamSeries(self, since, untill):
	
        try:
                connection = pyodbc.connect(self.connectionString(self.server, self.db, self.uid, self.pwd))
                cursor = connection.cursor()
        except:
                print "Connection to server failed!"
                return -1

        query = "SELECT TIMESTAMP, VALUE FROM " + self.cparser.currentSteamTable() + " WHERE TIMESTAMP > '" + str(since)[:23] + "' AND TIMESTAMP <'" + str(untill)[:23] + "' ORDER BY TIMESTAMP" 

        try:
                cursor.execute(query)
        except:
                print query
                print "Unvalid Query to the database"
                return -1

        entries = cursor.fetchall()

        data = {}
        for e in entries:
            data[e.TIMESTAMP] = e.VALUE

        cursor.close()
        connection.close()
        return data

    def commitForecast(self, forecast):

	try:
	    connection = pyodbc.connect(self.connectionString(self.server, self.db, self.uid, self.pwd))
	    cursor = connection.cursor()
	except:
	    print "Connection to server failed!"
	    return -1

	query = "INSERT INTO " + self.preheatForecastTable + " (Run_DateTime, Prediction_DateTime) VALUES ('" + str(datetime.datetime.now())[0:23] + "', '" + str(forecast)[0:23] + "')"

	#print query

	try:
	    cursor.execute(query)
	    cursor.commit()
	except:
	    print "Commiting forecast failed!"
	    return -1
	
	cursor.close()
	connection.close()
