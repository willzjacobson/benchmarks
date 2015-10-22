
import sys
import optparse
import cfgparse

from common_rudin.common import log_from_config, setup, setup_cparser
import common_rudin.utils as utils

import pyodbc

import datetime as dt

import numpy

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D

from sklearn.mixture import GMM
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import ExtraTreesRegressor

from scipy import interpolate

import pickle

import traceback

_module = 'thermal_mdp'


class DatabaseInterface:

	def __init__(self, server, database, db_uid, db_pwd):
		self.connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(server, database, db_uid, db_pwd)) 
	#_keys = [(Floor_1, Quadrant_1), (Floor_2, Quadrant_2), ..., (Floor_n, Quadrant_n)]
	def get_bms_series(self, tables, _from, _to, _group='ALL', _discrete=False, _keys=None, _domain=(-numpy.inf, numpy.inf), last=False):
		
		cursor = self.connection.cursor()
		if not(isinstance(tables, list)):
			tables = [tables]

		unprocessed_dataset = []
		for table in tables:

			query = "SELECT DISTINCT ZONE, FLOOR, QUADRANT, EQUIPMENT_NO FROM [{0}] WHERE TIMESTAMP >= '{1}' AND TIMESTAMP <= '{2}'"
			query = query.format(table, _from, _to)
			cursor.execute(query)
			pointnames = cursor.fetchall()
	
			for p in pointnames:
				pointname = table[:3] + str(p.ZONE) + str(p.FLOOR) + str(p.QUADRANT) + table[12:27] + str(p.EQUIPMENT_NO) + table[30:]
				query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE ZONE='{1}' AND FLOOR='{2}' AND QUADRANT='{3}' AND EQUIPMENT_NO='{4}' AND TIMESTAMP > '{5}' AND TIMESTAMP < '{6}' ORDER BY TIMESTAMP"
				key_flag = True
				if _keys != None:
					key_flag = False
					for _floor, _quadrant in _keys:
						if str(p.FLOOR) == _floor and str(p.QUADRANT) == _quadrant:
							key_flag = True
							break
				if not(key_flag):
					continue
				query = query.format(table, p.ZONE, p.FLOOR, p.QUADRANT, p.EQUIPMENT_NO, _from, _to)
				cursor.execute(query)
				entries = cursor.fetchall()
				print pointname + ": " + str(len(entries)) + " points"
				x = []
				y = []
				for e in entries:
					if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):
						continue 
					#x.append(e.TIMESTAMP)
					ts = str(e.TIMESTAMP)
					timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
					x.append(timestamp)
					y.append(e.VALUE)

				# dealing with void
				if last:	
					timestamp = dt.datetime.strptime(str(_to)[:19], "%Y-%m-%d %H:%M:%S")
					unprocessed_dataset.append([pointname, [timestamp], [y[-1]], _group, _discrete])
				else:
					unprocessed_dataset.append([pointname, x, y, _group, _discrete])

		cursor.close()
		return unprocessed_dataset
	
	# ag2818: for series with data overlapping in time
	def get_overlapping_series(self, tables, _from, _to, _group='ALL',
			_discrete=False, _keys=None, _domain=(-numpy.inf, numpy.inf),
			last=False):
		
		cursor = self.connection.cursor()
		if not(isinstance(tables, list)):
			tables = [tables]

		unprocessed_dataset = []
		for table in tables:

			query = "SELECT DISTINCT ZONE, FLOOR, QUADRANT, EQUIPMENT_NO FROM [{0}] WHERE TIMESTAMP >= '{1}' AND TIMESTAMP <= '{2}'"
			query = query.format(table, _from, _to)
			cursor.execute(query)
			pointnames = cursor.fetchall()
	
			for p in pointnames:
				pointname = table[:3] + str(p.ZONE) + str(p.FLOOR) + str(p.QUADRANT) + table[12:27] + str(p.EQUIPMENT_NO) + table[30:]
				#query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE ZONE='{1}' AND FLOOR='{2}' AND QUADRANT='{3}' AND EQUIPMENT_NO='{4}' AND TIMESTAMP > '{5}' AND TIMESTAMP < '{6}' ORDER BY TIMESTAMP"
				query = """SELECT t1.TIMESTAMP, t1.VALUE
					FROM [{0}] t1,
						(SELECT  MAX(Runtime) Runtime, TIMESTAMP
							FROM [{0}]
							WHERE Floor = '{2}' AND Quadrant = '{3}'
								AND EQUIPMENT_NO = '{4}'
							GROUP BY TIMESTAMP) t2
					WHERE t1.Floor = '{2}' AND t1.Quadrant = '{3}'
						AND t1.EQUIPMENT_NO = '{4}'
						AND t1.Runtime = t2.Runtime
						AND t1.TIMESTAMP = t2.TIMESTAMP
						AND t1.TIMESTAMP > '{5}' AND t1.TIMESTAMP < '{6}'
					ORDER BY t1.TIMESTAMP"""
				key_flag = True
				if _keys != None:
					key_flag = False
					for _floor, _quadrant in _keys:
						if str(p.FLOOR) == _floor and str(p.QUADRANT) == _quadrant:
							key_flag = True
							break
				if not(key_flag):
					continue
				query = query.format(table, p.ZONE, p.FLOOR, p.QUADRANT, p.EQUIPMENT_NO, _from, _to)
				cursor.execute(query)
				entries = cursor.fetchall()
				print pointname + ": " + str(len(entries)) + " points"
				x = []
				y = []
				for e in entries:
					if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):
						continue 
					#x.append(e.TIMESTAMP)
					ts = str(e.TIMESTAMP)
					timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
					x.append(timestamp)
					y.append(e.VALUE)

				# dealing with void
				if last:	
					timestamp = dt.datetime.strptime(str(_to)[:19], "%Y-%m-%d %H:%M:%S")
					unprocessed_dataset.append([pointname, [timestamp], [y[-1]], _group, _discrete])
				else:
					unprocessed_dataset.append([pointname, x, y, _group, _discrete])

		cursor.close()
		return unprocessed_dataset
	


	def get_generic_series(self, (table, table_alias), time_column, value_columns, _from, _to, _group='ALL', _discrete=False, _domain=(-numpy.inf, numpy.inf)):
		
		cursor = self.connection.cursor()
		unprocessed_dataset = []

		for value_column, value_column_alias in value_columns:
			pointname = table_alias + "_" + value_column_alias
			query = "SELECT {0} AS TIMESTAMP, {1} AS VALUE FROM [{2}] WHERE {3} >= '{4}' AND {5} <= '{6}' ORDER BY {7}"
			query = query.format(time_column, value_column, table, time_column, _from, time_column, _to, time_column) 
			cursor.execute(query)
			entries = cursor.fetchall()
			print pointname + ": " + str(len(entries)) + " points"
			x = []
			y = []
			for e in entries:
				if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):
					continue
				ts = str(e.TIMESTAMP)
				timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
				x.append(timestamp) 
				y.append(e.VALUE)
			unprocessed_dataset.append([pointname, x, y, _group, _discrete])


		cursor.close()
		return unprocessed_dataset

	def get_bms_forecast(self, (table, table_alias), meta_time_column, time_column, value_columns, _time, _before, _group='ALL', _discrete=False, _domain=(-numpy.inf, numpy.inf)):
		
		cursor = self.connection.cursor()
		unprocessed_dataset = []

		for value_column, value_column_alias in value_columns:
			pointname = table_alias + "_" + value_column_alias
			query = "SELECT {0} AS TIMESTAMP, {1} AS VALUE FROM ([{2}] a INNER JOIN (SELECT MAX({3}) as most_recent FROM [{4}] WHERE {5} <= '{6}') b ON a.{7} = b.most_recent) WHERE {8} < '{9}' ORDER BY {10}" 
			query = query.format(time_column, value_column, table, meta_time_column, table, meta_time_column, _time, meta_time_column, time_column, _before, time_column) 
			
			cursor.execute(query)
			entries = cursor.fetchall()
			print pointname + ": " + str(len(entries)) + " points"
			x = []
			y = []
			for e in entries:
				if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):	
					continue
				ts = str(e.TIMESTAMP)
				timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
				x.append(timestamp)
				y.append(e.VALUE)
			unprocessed_dataset.append([pointname, x, y, _group, _discrete])

		cursor.close()
		return unprocessed_dataset


	def commit_bms_series(self, table, time, pointname, timestamps, values):

		cursor = self.connection.cursor()
		zone = pointname[3:6]
		floor = pointname[6:9]
		quadrant = pointname[9:12]
		equipment = pointname[27:30]

		for timestamp, value in zip(timestamps, values):
			query = "INSERT INTO [{0}] (ZONE, FLOOR, QUADRANT, EQUIPMENT_NO, TIMESTAMP, VALUE, RUNTIME) VALUES('{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}')"
			query = query.format(table, zone, floor, quadrant, equipment, str(timestamp)[:19], value, time)	
			cursor.execute(query)

		cursor.commit()
		cursor.close()



	def get_forecast_series(self, (table, table_alias), meta_time_column, time_column, value_columns, _time, _before, _group='ALL', _discrete=False, _domain=(-numpy.inf, numpy.inf)):
		
		cursor = self.connection.cursor()
		unprocessed_dataset = []

		for value_column, value_column_alias in value_columns:
			pointname = table_alias + "_" + value_column_alias
			query = "SELECT {0} AS TIMESTAMP, {1} AS VALUE FROM ([{2}] a INNER JOIN (SELECT MAX({3}) as most_recent FROM [{4}] WHERE {5} <= '{6}') b ON a.{7} = b.most_recent) WHERE {8} < '{9}' ORDER BY {10}" 
			query = query.format(time_column, value_column, table, meta_time_column, table, meta_time_column, _time, meta_time_column, time_column, _before, time_column) 
			
			cursor.execute(query)
			entries = cursor.fetchall()
			print pointname + ": " + str(len(entries)) + " points"
			x = []
			y = []
			for e in entries:
				if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):	
					continue
				ts = str(e.TIMESTAMP)
				timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
				x.append(timestamp)
				y.append(e.VALUE)
			unprocessed_dataset.append([pointname, x, y, _group, _discrete])

		cursor.close()
		return unprocessed_dataset


	def commit_bms_series(self, table, time, pointname, timestamps, values):

		cursor = self.connection.cursor()
		zone = pointname[3:6]
		floor = pointname[6:9]
		quadrant = pointname[9:12]
		equipment = pointname[27:30]

		for timestamp, value in zip(timestamps, values):
			query = "INSERT INTO [{0}] (ZONE, FLOOR, QUADRANT, EQUIPMENT_NO, TIMESTAMP, VALUE, RUNTIME) VALUES('{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}')"
			query = query.format(table, zone, floor, quadrant, equipment, str(timestamp)[:19], value, time)	
			cursor.execute(query)

		cursor.commit()
		cursor.close()

	def __del__(self):
		self.connection.close()


class DataFrame:

	def __init__(self):
		self.raw = []
		self.X = []
		self.pointnames = []
		self.timestamps = []
		self.Type = []
		self.group = {}
		self.covarSize = 0
		self.pointSize = 0


	def set(self, X, pointnames, timestamps, group):

		self.X = X
		self.pointnames = pointnames
		self.timestamps = timestamps
		self.covarSize = len(pointnames)
		self.pointSize = len(timestamps)
		self.group = group


	def add_series(self, series, _from=None, _to=None, granularity=15):
		self.raw += series

		self.process(_from, _to, granularity)
		#self.normalize()


	def align(self):

		all_timestamps = []
		for [pointname, timestamps, values, group, discrete], i in zip(self.raw, xrange(len(self.raw))):
			all_timestamps += timestamps
			self.pointnames.append(pointname)
			try:
				self.group[group].append(i)
			except:
				self.group[group] = [i]
		all_timestamps = set(all_timestamps)
		all_timestamps = sorted(list(all_timestamps))
		T = len(all_timestamps)
		self.covarSize = len(self.pointnames)

		self.X = numpy.random.rand(T, self.covarSize)*0 - 9999

		tim_index = {}
		for t, i in zip(all_timestamps, xrange(T)):
			time_index[t] = i

		for [pointname, timestamps, values, group, discrete], i in zip(self.raw, xrange(len(self.raw))):
			for v, t in zip(timestamps, values):
				self.X[time_index[t], i] = v


	def refine(self, group, base_groups, max_flat_line = 20):

		refI = []
		for g in base_groups:
			refI += self.group[g]
		refI = sorted(list(set(refI)))

		refX = numpy.array([self.X.T[i] for i in refI]).T

		for i in self.group[group]:
			y = self.X.T[i]

			freezed_value = y[0]
			freezed_time = self.timestamps[0]
			freezed_index = 0
			
			gapI = []

			for t, v , j in zip(self.timestamps, y, xrange(self.pointSize)):

				if v != freezed_value:
					duration = t - freezed_time
					duration_flat_line = duration.days*24 + duration.seconds//3600
					if duration_flat_line >= max_flat_line: 	
						gapI += range(freezed_index, j)

					freezed_index = j
					freezed_value = v
					freezed_time = t

			validI = list(set(range(0, self.pointSize)).difference(set(gapI)))
			validY = numpy.array([y[k] for k in validI])
			validX = numpy.array([refX[k] for k in validI])
			gapX = numpy.array([refX[k] for k in gapI])
			est = ExtraTreesRegressor()
			est.fit(validX, validY)
			gapY = est.predict(gapX)

			for j, k in zip(gapI, xrange(len(gapY))):
				self.X[j, i] = gapY[k]
			

	def process(self, _from, _to, granularity):
		ud = self.raw 
		all_timestamps = set([])
		pointnames = []
		for [pointname, timestamps, values, _group, discrete], i in zip(ud, xrange(len(ud))):
			all_timestamps = all_timestamps.union(set(timestamps))
			pointnames.append(pointname)
			try:
				self.group[_group].append(i)
			except:
				self.group[_group] = [i]

			if discrete:
				self.Type.append('discrete')
			else:
				self.Type.append('continuous') 

		all_timestamps = sorted(list(all_timestamps))

		if _from == None and _to == None:
			base = min(all_timestamps)
			end = max(all_timestamps)

		else:
			base = _from
			end = _to

		timestamps = []
		timestamps_offset = []

		while True:
			base += dt.timedelta(0, 1)
			if base.minute % 15 == 0 and base.second == 0:
				break
		while True:
			end += dt.timedelta(0, 1)
			if end.minute %15 == 0 and end.second == 0:
				break

		current = base
		current_offset = 0

		while current <= end:
			timestamps.append(current)
			timestamps_offset.append(current_offset)
			current += dt.timedelta(0, granularity * 60)
			current_offset += granularity

		matrix = []

		for [pointname, ts, values, group, discrete] in ud:
			x = []
			for t in ts:
				offset = t-base
				x.append(offset.days * 24 * 60 + offset.seconds / 60)
			x = [timestamps_offset[0]] + x + [timestamps_offset[-1]]
			aug_values = [values[0]] + values + [values[-1]]

			#interpolated_values = numpy.interp(timestamps_offset, x, values)
			#matrix.append(list(interpolated_values))

			#function = interpolate.interp1d(x, aug_values, kind='linear')
			function = interpolate.interp1d(x, aug_values, kind='nearest')
			interpolated_values = function(timestamps_offset)

			nan_flag = numpy.nan in interpolated_values or numpy.inf in interpolated_values


			if discrete or nan_flag:
				#function = interpolate.interp1d(x, aug_values, kind='nearest')	
				function = interpolate.interp1d(x, aug_values, kind='zero')	
				interpolated_values = function(timestamps_offset)
				nan_flag = numpy.nan in interpolated_values or numpy.inf in interpolated_values

			if nan_flag:
				print "NAN value for {0}".format(pointname)
	

			matrix.append(list(interpolated_values))

		matrix = numpy.matrix(matrix)
		matrix = numpy.asarray(matrix)
		X = matrix.transpose()
		X = numpy.asarray(X)

		self.X = X
		self.pointnames = pointnames
		self.timestamps = timestamps
		self.pointSize = len(self.timestamps)
		self.covarSize = len(self.pointnames)

		time_covar = numpy.array([[t.hour*60 + t.minute, t.weekday()] for t in self.timestamps])
		self.X = numpy.concatenate((self.X, time_covar), axis=1)
		self.pointnames.append('minute')
		self.pointnames.append('weekday')
		self.group['time'] = [self.covarSize, self.covarSize+1]
		self.covarSize += 2
		self.Type += ['continuous', 'continuous']



	def plot(self, groups = []):

		if groups == []:
			groups = self.group.keys()

		if not(isinstance(groups, list)):
			groups = [groups]

		fig, ax = plt.subplots()
		for g in groups:
			for i in self.group[g]:
				ax.plot(self.timestamps, self.X.T[i])
		plt.show()
	
	def normalize(self):

		matrix = numpy.matrix(self.X)
		matrix = matrix.transpose()
		matrix = numpy.asarray(matrix)

		for i in xrange(len(matrix)):
			matrix[i] -= numpy.min(matrix[i])
			matrix[i] /= numpy.max(matrix[i])

		matrix = numpy.matrix(matrix)
		matrix = matrix.transpose()
		self.X = matrix


	def csv(self):
		File = open('snapshot.csv', 'w')
		File.write("Timestamp, ")
		for i in range(0, len(self.pointnames)-1):
			File.write(self.pointnames[i] + ", ")
		File.write(self.pointnames[-1] + '\n')

		for i in range(0, len(self.X)):
			File.write(str(self.timestamps[i]) + ", ")
			for j in range(0, len(self.X[i])-1):
				File.write(str(self.X[i][j]) + ", ")
			File.write(str(self.X[i][-1]) + '\n')


	def subset(self, _from, _to):
		
		df = DataFrame()
	
		if isinstance(_from, int) and isinstance(_to):
			df.set(self.X[_from:_to], self.pointnames, self.timestamps[_from:_to], self.group)
			df.Type = self.Type

		if isinstance(_from, dt.datetime) and isinstance(_to, dt.datetime):

			indices = []
			for i in xrange(self.pointSize):
				if self.timestamps[i] >= _from and self.timestamps[i] <= _to:
					indices.append(i)

			print [indices[0], indices[-1]]

			newX = numpy.array([self.X[i] for i in indices])
			newT = [self.timestamps[i] for i in indices]
			df.set(newX, self.pointnames, newT, self.group)
			df.Type = self.Type

		return df


	def merge(self, df, override=True):

		if not(self.pointnames == df.pointnames):
			return

		if override:
			for i in reversed(xrange(len(self.timestamps))):
				if self.timestamps[i] > df.timestamps[0]:
					continue
				else:
					self.timestamps = self.timestamps[:i+1] + df.timestamps
					self.X = numpy.concatenate((self.X[:i+1], df.X), axis=0)
					break

		else:
			self.timestamps += df.timestamps
			self.X = numpy.concatenate((self.X, df.X), axis=0)

		sorted_index = [i[1] for i in sorted(zip(self.timestamps, xrange(len(self.timestamps))))]
		self.timestamps = [self.timestamps[i] for i in sorted_index]
		self.X = numpy.array([self.X[i] for i in sorted_index])

		self.pointSize = len(self.timestamps)


class MarkovRandomizedTree:

	def __init__(self, dataframe):

		self.Estimator = {}
		self.Dependency = {}

		self.covarname = dataframe.pointnames
		self.covarsize = dataframe.covarSize
		self.group = dataframe.group
		self.Type = dataframe.Type
	
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


	def fit(self, X):
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

	
		print odf.timestamps[0]
		
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

		pdf = DataFrame()
		pdf.set(PX, self.covarname, time, self.group)
		return pdf


########################

def cost(df, factorize=False):

	tau = numpy.random.rand(24)
	eta = numpy.random.rand(24)
	sigma = numpy.random.rand(24)

	opening_hour = 7
	closing_hour =  19

	granularity = 15

	Cost = 0

	temp_violation = 0
	temp_penalty = 0
	steam_cost = 0
	electric_cost = 0
	energy_cost = 0

	for i in xrange(24):

		if i >=6 and i < 19:
			sigma[i] = 10 * 26.5 * granularity/60
		else:
			sigma[i] = 26.5 * granularity/60 

		eta[i] = 0.2 * granularity/60

		if i >= 7 and i < 19:
			tau[i] = 1000
		else:
			tau[i] = 0

	for t in xrange(df.pointSize):
		hour = df.timestamps[t].hour

		for i in df.group['temp']:
			violation = 0
			temp = df.X[t, i]
			if temp >= 72 and temp <= 75:
				violation = 0
			elif temp >= 70 and temp <= 77:
				violation = 20 * min([abs(77-temp), abs(72-temp)])
			else:
				violation = 100 * min([abs(77-temp), abs(72-temp)])
	
			temp_penalty += tau[hour] * violation * violation 

			
			violation = 0
			temp = df.X[t, i]
			if temp >= 72 and temp <= 75:
				violation = 0		
			else:
				violation = min([abs(75-temp), abs(72-temp)])
			temp_violation += (tau[hour]/1000) * violation/len(df.group['temp']) /4*12
		
	
		

		for i in df.group['electric']:
			electric_cost += eta[hour] * df.X[t, i]

		for i in df.group['steam']:
			steam_cost += sigma[hour] * df.X[t, i]

	energy_cost = steam_cost + electric_cost

	alpha = 1
	beta = 1

	objective = energy_cost + temp_penalty

	if factorize:
		return [temp_penalty, temp_violation, electric_cost, steam_cost, energy_cost, objective]
	else:
		return objective

#def search(_from, _to):
def search(argv):

	#return	
	#_to = dt.datetime.now()
	if len(argv) == 1:
		_to = dt.datetime.now()
	else:
		_to = argv
	_from = _to - dt.timedelta(365)

	_to = str(_to)[:19]
	_from = str(_from)[:10]

	bms_server = "anderson.ldeo.columbia.edu"
	bms_database = "345"
	bms_user = "Hooshmand"
	bms_pwd = "Breakit68"

	weather_server = "anderson.ldeo.columbia.edu"
	weather_database = "Weather"
	weather_user = "Hooshmand"
	weather_pwd = "Breakit68"

	weather_table = 'Observations_History'
	weather_fcst_table = 'Hourly_Forecast'

	tpo_server = "anderson.ldeo.columbia.edu"
	tpo_database = "345"
	tpo_user = "Hooshmand"
	tpo_pwd = "Breakit68"

	# group name: table, discrete, domain, control;
	fan_table = '345---------001BMSHVAFANLCP---VAL001'
	pum_table = '345---------001BMSWATSECPUM---VAL001'
	tem_table = '345---------001BMSHVATEMSPA---VAL001'
	ele_table = '345---------001BMSELEMET------VAL001'
	ste_table = '345---------001BMSSTEMET------VAL001'
	occ_table = '345---------000SECCNTPEOBUI---VAL001'

	Floors = 'F02, F04, F04, F05, F13, F18, F20, F24, F32, F38, F40'
	Quadrants= 'CNW, CNW, CSE, CSE, CSW, CSE, CSW, CSE, CNW, CNW, CNE'

	fan_rec_table = '345---------001TPOHVAFANLCP---VAL001'
	pum_rec_table = '345---------001TPOWATSECPUM---VAL001'

	horizon= 24

	Floors = Floors.replace(' ', '').split(',')
	Quadrants = Quadrants.replace(' ', '').split(',')

	temp_keys = zip(tuple(Floors), tuple(Quadrants))

	################################################

	bms_interface = DatabaseInterface(bms_server, bms_database, bms_user, bms_pwd)
	s = []
	# Actions
	s += bms_interface.get_bms_series(fan_table, _from, _to, _group='fan', _discrete=True)
	s += bms_interface.get_bms_series(pum_table, _from, _to, _group='pump', _discrete=True)

	# States
	s += bms_interface.get_bms_series(tem_table, _from, _to, _keys=temp_keys, _group='temp', _domain=(0, 120))

	s += bms_interface.get_bms_series(ele_table, _from, _to, _group='electric', _domain=(0, 1500))
	s += bms_interface.get_bms_series(ste_table, _from, _to, _group='steam')
	s += bms_interface.get_bms_series(occ_table, _from, _to, _group='occupancy')

	weather_interface = DatabaseInterface(weather_server, weather_database, weather_user, weather_pwd)
	s += weather_interface.get_generic_series((weather_table, "Weather"), "Date", [("TempA", "Temp"), ("DewPointA", "DewPoint"), ("Humidity", "Humidity")], _from, _to, _group='weather')

	df = DataFrame()
	df.add_series(s)

	df.refine("occupancy", ["weather", "time"])

	mrt = MarkovRandomizedTree(df)	
	mrt.addDependency('time', 'time')
	mrt.addDependency('occupancy', ['occupancy', 'time', 'weather'])
	mrt.addDependency('electric', ['electric', 'occupancy', 'fan', 'time'])
	mrt.addDependency('steam', ['steam', 'pump', 'pumpsm', 'time'])
	mrt.addDependency('temp', ['temp', 'weather', 'fan', 'pump', 'steam', 'time'])
	mrt.addDependency('weather', ['weather', 'time'])


	form = "%Y-%m-%d"
	_from = dt.datetime.strptime(_from, form)
	_to = dt.datetime.strptime(_to, form+" %H:%M:%S")

	##################################################

	print "Retrieving weather forecast data..."

	ndf = df.subset(_from, _to)
	_before = str(_to + dt.timedelta(horizon/24, horizon%24))[:19]
	t = weather_interface.get_forecast_series((weather_fcst_table, "Weather"), "Fcst_date", "Date", [("TempA", "Temp"), ("DewA", "DewPoint"), ("Humidity", "Humidity")], _to, _before, _group='weather')

	print "Retrieving lastest states of actions..."

	t += bms_interface.get_bms_series(fan_table, _from, _to, _group='fan', _discrete=True, last=True)
	t += bms_interface.get_bms_series(pum_table, _from, _to, _group='pump', _discrete=True, last=True)

	odf = DataFrame()
	odf.add_series(t)
	print odf.pointSize

	PDF = []
	#mrt.setDataFrame(ndf)
	mrt.fit(ndf.X)

	#print "Serializeing the model..."
	#model_file = open('model.txt', 'wb')
	#pickle.dump(mrt, model_file)
	#model_file.close()
	#print "Model successfully serialized."

	#t = 6*ndf.pointSize/8
	t = 0
	max_cost = numpy.inf
	costs = []
	while t < ndf.pointSize:
		print odf.X
		print ndf.timestamps[t]
		pdf = mrt.predict(ndf.timestamps[-1], ndf.X[-1], observations=odf)
		c = cost(pdf)
		
		costs.append(c)
		PDF.append(pdf)


		i_time2 = ndf.pointnames.index("minute")
		i_time1 = odf.pointnames.index("minute")

		while t < ndf.pointSize and ndf.X[t][i_time2] != odf.X[0][i_time1]:
			t += 1

		for i1 in odf.group['fan'] + odf.group['pump']:
			i2 = ndf.pointnames.index(odf.pointnames[i1])
			for pointer in xrange(odf.pointSize):
				if t + pointer < ndf.pointSize:
					odf.X[pointer][i1] = ndf.X[t+pointer][i2]

		t += 1


	_from += dt.timedelta(0, 12 * 60 * 60)
	_to += dt.timedelta(0, 12 * 60 * 60)

	costs = numpy.array(costs)
	costs -= numpy.min(costs)
	costs /= numpy.max(costs)

	##################################################

	bestPDF = None

	for pdf, _c1 in zip(PDF, costs):
		if _c1 == 0:
			bestPDF = pdf

	now = str(dt.datetime.now())[:19]
	#now = str(argv)[:19]
	
	for g in ['fan', 'pump', 'electric', 'temp', 'steam', 'occupancy']:

		table = ''
		if g == 'fan':
			table = fan_rec_table
		elif g == 'pump':
			table = pum_rec_table

		else:
			table = 'asc_output_' + g

		for i in bestPDF.group[g]:
			print "Commiting to " + table + "..."
			bms_interface.commit_bms_series(table, now, bestPDF.pointnames[i], bestPDF.timestamps, bestPDF.X.T[i])
			print "Sucessful!"



if __name__ == '__main__':

	now = str(dt.datetime.now())[:19]
	#search('2014-01-01', now)
	search(sys.argv)
	#f = open("model.txt", 'rb')
	#mrt = pickle.load(f)

