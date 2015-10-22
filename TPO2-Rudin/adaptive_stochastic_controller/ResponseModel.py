import datetime as dt

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import ExtraTreesClassifier

import numpy

import DataFrame as DF

class MarkovRandomizedTree:

	def __init__(self, dataframe):

		self.Estimator = {}
		self.Dependency = {}

		self.dataframe = dataframe

		#self.covarname = dataframe.pointnames
		#self.covarsize = dataframe.covarSize
		#self.group = dataframe.group
		#self.Type = dataframe.Type
		#self.X = dataframe.X	
	
		self.fullDependency()	


	def fullDependency(self):

		for i in xrange(self.dataframe.covarSize):
			self.Dependency[i] = range(0, self.dataframe.covarSize)


	def addDependency(self, _from, _to):

		if not(isinstance(_from, list)):
			_from = [_from]

		for frm in _from:
			dependent = []
			if frm in self.dataframe.pointnames: 
				dependent.append(self.dataframe.pointnames.index(frm))
			elif frm in self.dataframe.group.keys():
				dependent += self.dataframe.group[frm]
			else:
				print "Keyword '{0}' not found".format(frm)


		if not(isinstance(_to, list)):
			_to = [_to]

		dependee = []
		for to in _to:
			if to in self.dataframe.pointnames: 
				dependee.append(self.dataframe.pointnames.index(to))
			elif to in self.dataframe.group.keys():
				dependee += self.dataframe.group[to]
			else:
				print "Keyword '{0}' not found".format(to)

		dependent = sorted(list(set(dependent)))
		dependee = sorted(list(set(dependee)))


		for dep in dependent:
			self.Dependency[dep] = dependee


	def fit(self):

		X = self.dataframe.X
		ix = []
		iy = []
		for i in xrange(len(self.dataframe.data_gaps_index)-1):
			if i == 0:
				ix += range(0, self.dataframe.data_gaps_index[i][0]-1)
				iy += range(1, self.dataframe.data_gaps_index[i][0])
			try:
				ix += range(self.dataframe.data_gaps_index[i][1], self.dataframe.data_gaps_index[i+1][0]-1)
				iy += range(self.dataframe.data_gaps_index[i][1]+1, self.dataframe.data_gaps_index[i+1][0])
			except:
				ix += range(self.dataframe.data_gaps_index[i][1], self.dataframe.pointSize-1)
				iy += range(self.dataframe.data_gaps_index[i][1]+1, self.dataframe.pointSize)	

		if ix == [] or iy ==[]:
			ix = range(0, self.dataframe.pointSize-1)
			iy = range(1, self.dataframe.pointSize)
					

		for i in xrange(self.dataframe.covarSize):
			print "Fitting covariate: {0}".format(self.dataframe.pointnames[i])
			x = numpy.array([X.T[j] for j in self.Dependency[i]]).T
			y = X.T[i]

			x = [x[index] for index in ix]
			y = [y[index] for index in iy]
			if self.dataframe.Type[i] == 'discrete':
				model = ExtraTreesClassifier()
				model.fit(x, y)
				self.Estimator[i] = model 

			else:
				model = ExtraTreesRegressor()
				model.fit(x, y)
				self.Estimator[i] = model 


	def predict(self, current_time, current, observations):

		odf = observations

		pairings = {}
		pairings_inverse = {}
		for i in xrange(odf.covarSize):
			if odf.pointnames[i] in self.dataframe.pointnames: 
				pairings[i] = self.dataframe.pointnames.index(odf.pointnames[i])
				pairings_inverse[self.dataframe.pointnames.index(odf.pointnames[i])] = i

	
		print odf.timestamps[0]
		
		PX = []
		PX.append(current)
		time = [current_time]
		for step, ts in zip(xrange(odf.pointSize), odf.timestamps):
			Next = current * 0
			for i in xrange(self.dataframe.covarSize):
				if i in pairings_inverse.keys():
					Next[i] = odf.X[step, pairings_inverse[i]]
					continue
				else:
					x = numpy.array([current[j] for j in self.Dependency[i]])
					Next[i] = self.Estimator[i].predict(x)

			PX.append(Next)
			current_time += dt.timedelta(0, 15*60)
			time.append(current_time)
			current = Next
	
		PX = numpy.array(PX)

		pdf = DF.DataFrame()
		pdf.set(PX, self.dataframe.pointnames, time, self.dataframe.group)
		return pdf



'''
class MarkovRandomizedTree:

	def __init__(self, dataframe):

		self.Estimator = {}
		self.Dependency = {}

		self.covarname = dataframe.pointnames
		self.covarsize = dataframe.covarSize
		self.group = dataframe.group
		self.Type = dataframe.Type

		self.X = dataframe.X

		self.gaps = dataframe.data_gaps
	
		self.fullDependency()	


	def fullDependency(self):

		for i in xrange(self.covarsize):
			self.Dependency[i] = range(0, self.covarsize)


	def addDependency(self, _from, _to):

		if not(isinstance(_from, list)):
			_from = [_from]

		for frm in _from:
			dependent = []
			if frm in self.covarname: 
				dependent.append(self.covarname.index(frm))
			elif frm in self.group.keys():
				dependent += self.group[frm]
			else:
				print "Keyword '{0}' not found".format(frm)


		if not(isinstance(_to, list)):
			_to = [_to]

		dependee = []
		for to in _to:
			if to in self.covarname: 
				dependee.append(self.covarname.index(to))
			elif to in self.group.keys():
				dependee += self.group[to]
			else:
				print "Keyword '{0}' not found".format(to)

		dependent = sorted(list(set(dependent)))
		dependee = sorted(list(set(dependee)))


		for dep in dependent:
			self.Dependency[dep] = dependee


	def fit(self):

		X = self.X

		for i in xrange(self.covarsize):
			print "Fitting covariate: {0}".format(self.covarname[i])
			x = numpy.array([X.T[j] for j in self.Dependency[i]]).T[:-1]
			y = X.T[i][1:]
			if self.Type[i] == 'discrete':
				model = ExtraTreesClassifier()
				model.fit(x, y)
				self.Estimator[i] = model 

			else:
				model = ExtraTreesRegressor()
				model.fit(x, y)
				self.Estimator[i] = model 


	def predict(self, current_time, current, observations):

		odf = observations

		pairings = {}
		pairings_inverse = {}
		for i in xrange(odf.covarSize):
			if odf.pointnames[i] in self.covarname: 
				pairings[i] = self.covarname.index(odf.pointnames[i])
				pairings_inverse[self.covarname.index(odf.pointnames[i])] = i

	
		#print odf.timestamps[0]
		
		PX = []
		PX.append(current)
		time = [current_time]
		for step, ts in zip(xrange(odf.pointSize), odf.timestamps):
			Next = current * 0
			for i in xrange(self.covarsize):
				if i in pairings_inverse.keys():
					Next[i] = odf.X[step, pairings_inverse[i]]
					continue
				else:
					x = numpy.array([current[j] for j in self.Dependency[i]])
					Next[i] = self.Estimator[i].predict(x)

			PX.append(Next)
			current_time += dt.timedelta(0, 15*60)
			time.append(current_time)
			current = Next
	
		PX = numpy.array(PX)

		pdf = DF.DataFrame()
		pdf.set(PX, self.covarname, time, self.group)
		return pdf

'''
