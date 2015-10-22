
import pyodbc
import sys, os
import numpy
import datetime
import matplotlib.pyplot as plt

from configParser import configParser
import mytools

class feature:
	
	def __init__(self, table, control):
		self.Table
		self.Control

class covMatrix:

	def __init__(self, connection, config_parser, data_retriever, interval):
		
		self.cparser = config_parser
		
		self.Connection = connection
		self.Cursor = self.Connection.cursor()
		
		self.DataRetriever = data_retriever
		
		self.Tables = self.cparser.measurementTables()
		self.Keys = self.cparser.compositeKeys()
		
		self.TimeAttribute = self.cparser.timeAttribute()
		self.ValueAttribute = self.cparser.valueAttribute()
		
		self.Interval = interval
		
		self.constructFeatures()
		
		for i in self.Features:
			print self.Features[i]
			
		self.constructCovariateMatrix()
		
	def setTables(self, tables_list):
		self.Tables = tables_list

	def setKeys(self, keys_list):
		self.Keys = keys_list
	
	def constructFeatures(self):
		
		# a single feature = ( table_name, zone_value, floor_value, quadrant_value, equipment_no_value )
		self.Features = {}
		self.FeatureSize = 0
		
		print "Scanning database for features..."
		
		for table in self.Tables:
			entries = self.DataRetriever.retrieve(table, columns=self.Keys, distinct=True)
			
			print "Scanning table " + table
			
			length = len(self.Keys)
			
			for entry in entries:
				command = "feature = (table, "
				end = False
				counter = 0
				for key in self.Keys:
					counter += 1
					end = counter == length
					command += "entry." + str(key)
					if not(end):
						command += ", "
					else:
						command += ")"
				exec(command)
				#feature = (table, entry.ZONE, entry.FLOOR, entry.QUADRANT, entry.EQUIPMENT_NO)
				self.Features[self.FeatureSize] = feature
				self.FeatureSize += 1
				
		print "Features Set Constructed Successfully..."
		
		
	def features(self):
		return self.Features
				
	def constructCovariateMatrix(self):
	
		self.TimeStamps = []
		self.Matrix = {}
		self.SharedTimestamps = set([])
		
		for feature in self.Features:
			
			row = {}
			
			constraints = {}
			index = 1
			for key in self.Keys:
				constraints[key] = self.Features[feature][index]
				index += 1
			#constraints[self.TimeAttribute] =(str(datetime.datetime(2013, 05, 01)), str(datetime.datetime(2013, 06, 01)))
			constraints[self.TimeAttribute] = self.Interval
			
			entries = self.DataRetriever.retrieve(table=self.Features[feature][0], columns=[self.TimeAttribute, self.ValueAttribute], constraints=constraints, orderby=[self.TimeAttribute])
			print "feature " + str(self.Features[feature][0]) + ": " + str(len(entries))
			
			for entry in entries:
				exec("timestamp = datetime.datetime(entry." + self.TimeAttribute + ".year, entry." + self.TimeAttribute + ".month, entry." + self.TimeAttribute + ".day, entry." + self.TimeAttribute + ".hour, entry." + self.TimeAttribute + ".minute)" )
				exec("value = entry." + self.ValueAttribute)
				
				#if timestamp in self.Matrix.keys():
				#	self.Matrix[timestamp][feature] = value
				#	
				#else:
				#	self.Matrix[timestamp] = {}
				#	self.Matrix[timestamp][feature] = value
				
				try:
					self.Matrix[timestamp][feature] = value
				except:
					self.Matrix[timestamp] = {}
					self.Matrix[timestamp][feature] = value
					
		#self.visualizeMatrix()
		self.convertMatrix()
	
	def getMatrix(self):
		return self.Matrix2D
		
	def getMatrixTranspose(self):
		
		self.MatrixTranspose = {}
		
		for feature in self.Features:
			self.MatrixTranspose[feature] = {}
		
		for time in self.Matrix:
			for feature in self.Matrix[time]:
				self.MatrixTranspose[feature][time] = self.Matrix[time][feature]
				
	def convertMatrix(self):
		
		self.Matrix2D = []
		
		for feature in self.Features:
			self.Matrix2D.append([])
		for time in sorted(self.Matrix.keys()):
			for feature in self.Features:
				try:
					value = self.Matrix[time][feature]
					self.Matrix2D[feature].append(value)
				except:
					self.Matrix2D[feature].append(-1)	
			
	def getTimeStamps(self):
		return self.Matrix.keys()
		
	def interval(self):
		return self.Interval
			
	def visualizeMatrix(self):
		self.convertMatrix()
		t = sorted(self.Matrix.keys())
		
		number = 111
		
		y = self.Matrix2D[0]
		
		fig = plt.figure()
		ax1 = fig.add_subplot(number)
		ax1.plot(t, y, '-b')
		ax1.set_xlabel('sequence')
		ax1.set_ylabel('temperature')
		
		for row in range(1, len(self.Matrix2D)):
			
			y = self.Matrix2D[row]
			#number += 1
			#fig = plt.figure()
			ax1 = fig.add_subplot(number)
			ax1.plot(t, y, 'k-', color=numpy.random.rand(3))

		plt.show()



