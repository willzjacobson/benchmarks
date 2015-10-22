
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

			function = interpolate.interp1d(x, aug_values, kind='linear')
			interpolated_values = function(timestamps_offset)

			nan_flag = numpy.nan in interpolated_values or numpy.inf in interpolated_values


			if discrete or nan_flag:
				function = interpolate.interp1d(x, aug_values, kind='nearest')
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

def test(_from, _to):
	d = DatabaseInterface("anderson.ldeo.columbia.edu", "345", "Hooshmand", "Breakit68")
	s = []
	# Actions
	s += d.get_bms_series("345---------001BMSHVAFANLCP---VAL001", _from, _to, _group='fan', _discrete=True)
	#s += d.get_bms_series("345---------001BMSHVAFANRHC---SPV001", _from, _to, _group='reheat', _discrete=False)
	#s += d.get_bms_series("345---------001BMSHVAPFASAT---SPV001", _from, _to, _group='setpoint')
	s += d.get_bms_series("345---------001BMSWATSECPUM---VAL001", _from, _to, _group='pump', _discrete=True)
	s += d.get_bms_series("345---------001BMSWATSECSMO---VAL001", _from, _to, _group='pumpsm', _discrete=True)


	# States
	s += d.get_bms_series("345---------001BMSHVATEMSPA---VAL001", _from, _to, _keys=[('F02', 'CNW'), ('F04', 'CNW'), ('F04', 'CSE'), ('F05', 'CSE'), ('F13', 'CSW'), ('F18', 'CSE'), ('F20', 'CSW'), ('F24', 'CSE'), ('F32', 'CNW'), ('F38', 'CNW'), ('F40', 'CNE')], _group='temp', _domain=(0, 120))

	s += d.get_bms_series("345---------001BMSELEMET------VAL001", _from, _to, _group='electric')
	s += d.get_bms_series("345---------001BMSSTEMET------VAL001", _from, _to, _group='steam')
	s += d.get_bms_series("345---------000SECCNTPEOBUI---VAL001", _from, _to, _group='occupancy')

	d2 = DatabaseInterface("anderson.ldeo.columbia.edu", "Weather", "Hooshmand", "Breakit68")
	s += d2.get_generic_series(("Observations_History", "Weather"), "Date", [("TempA", "Temp"), ("DewPointA", "DewPoint"), ("Humidity", "Humidity")], _from, _to, _group='weather')

	df = DataFrame()
	df.add_series(s)
	df.refine("occupancy", ["weather", "time"])

	mrt = MarkovRandomizedTree(df)
	
	mrt.addDependency('time', 'time')
	#mrt.addDependency('fan', ['fan', 'time', 'weather'])
	#mrt.addDependency('reheat', ['reheat', 'time', 'weather'])
	#mrt.addDependency('pump', ['pump', 'time', 'weather'])
	#mrt.addDependency('pumpsm', ['pumpsm', 'time', 'weather'])
	#mrt.addDependency('setpoint', ['setpoint', 'time'])

	mrt.addDependency('occupancy', ['occupancy', 'time', 'weather'])

	mrt.addDependency('electric', ['electric', 'occupancy', 'fan', 'time'])
	mrt.addDependency('steam', ['steam', 'pump', 'pumpsm', 'time'])
	mrt.addDependency('temp', ['temp', 'weather', 'fan', 'pump', 'steam', 'time'])
	mrt.addDependency('weather', ['weather', 'time'])

	pdf = []
	n = 14

	form = "%Y-%m-%d"
	_from = dt.datetime.strptime(_from, form)
	_to = dt.datetime.strptime(_to, form+" %H:%M:%S")	
	_to -= dt.timedelta(n + 1)

	###########

	for ite in range(0, n):

		ndf = df.subset(_from, _to)
		# up to 24 hours
		_before = str(_to + dt.timedelta(1))[:19]

		t = d2.get_forecast_series(("Hourly_Forecast", "Weather"), "Fcst_date", "Date", [("TempA", "Temp"), ("DewA", "DewPoint"), ("Humidity", "Humidity")], _to, _before, _group='weather')
		odf = DataFrame()
		odf.add_series(t)
		#forecast_from = str(ndf.timestamps[-1] - dt.timedelta(0, 15*60))[:19]
		forecast_from = str(ndf.timestamps[-1])[:19]
		forecast_to = str(odf.timestamps[-1])[:19]

		t += d.get_bms_series("345---------001BMSHVAFANLCP---VAL001", forecast_from, forecast_to, _group='fan', _discrete=True)
		#t += d.get_bms_series("345---------001BMSHVAFANRHC---SPV001", forecast_from, forecast_to, _group='reheat', _discrete=True)
		t += d.get_bms_series("345---------001BMSWATSECPUM---VAL001", forecast_from, forecast_to, _group='pump', _discrete=True)
		t += d.get_bms_series("345---------001BMSWATSECSMO---VAL001", forecast_from, forecast_to, _group='pumpsm', _discrete=True)

		odf = DataFrame()
		odf.add_series(t)
	
		#mrt.setDataFrame(ndf)
		mrt.fit(ndf.X)
		p = mrt.predict(ndf.timestamps[-1], ndf.X[-1], observations=odf)

		if ite == 0:
			pdf = p
		else:
			pdf.merge(p)

		_from += dt.timedelta(0, 12 * 60 * 60)
		_to += dt.timedelta(0, 12 * 60 * 60)


	c = {}
	for pointname in df.pointnames:
		c[pointname] = numpy.floor(numpy.random.rand(3) * 5)/5

	groups = ['occupancy', 'electric', 'steam', 'temp']
	unitsm = ['Occupancy', 'Electric Load ($kW$)', 'Steam Demand ($Mlb$/$h$)', 'Temperatrue ($^{\circ}F$)']
	titles = ['Occupancy', 'Electric Consumption', 'Steam Demand', 'Interior Space Temperature']
	for group, unitm, title in zip(groups, unitsm, titles):
			
		fig, ax = plt.subplots()

		for x, name, i in zip(df.X.T, df.pointnames, xrange(df.covarSize)):
			if not(i in df.group[group]):
				continue
			_c = None
			try:
				_c = c[name]
			except:
				_c = numpy.random.rand(3)
		
			ax.plot(df.timestamps, x, color=_c)
		for x, name, i in zip(pdf.X.T, pdf.pointnames, xrange(pdf.covarSize)):
			if not(i in pdf.group[group]):
				continue
			_c = None
			try:
				_c = c[name]
			except:
				_c = numpy.random.rand(3)
		
			ax.plot(pdf.timestamps, x, '--', color=_c)

		plt.xlabel('time')
		plt.ylabel(unitm)
		plt.title(title)
		
	plt.show()


def cost(df):

	tau = numpy.random.rand(24)
	eta = numpy.random.rand(24)
	sigma = numpy.random.rand(24)

	opening_hour = 7
	closing_hour =  19

	granularity = 15

	Cost = 0

	for i in xrange(24):

		eta[i] = 0.2 * granularity/60
		sigma[i] = 26.5 * granularity/60

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

			Cost += tau[hour] * violation * violation 

		for i in df.group['electric']:
			Cost += eta[hour] * df.X[t, i]

		for i in df.group['steam']:
			Cost += sigma[hour] * df.X[t, i]

	return Cost

def search(_from, _to):

	d = DatabaseInterface("anderson.ldeo.columbia.edu", "345", "Hooshmand", "Breakit68")
	s = []
	# Actions
	s += d.get_bms_series("345---------001BMSHVAFANLCP---VAL001", _from, _to, _group='fan', _discrete=True)
	#s += d.get_bms_series("345---------001BMSHVAFANRHC---SPV001", _from, _to, _group='reheat', _discrete=False)
	#s += d.get_bms_series("345---------001BMSHVAPFASAT---SPV001", _from, _to, _group='setpoint')
	s += d.get_bms_series("345---------001BMSWATSECPUM---VAL001", _from, _to, _group='pump', _discrete=True)
	s += d.get_bms_series("345---------001BMSWATSECSMO---VAL001", _from, _to, _group='pumpsm', _discrete=True)


	# States
	s += d.get_bms_series("345---------001BMSHVATEMSPA---VAL001", _from, _to, _keys=[('F02', 'CNW'), ('F04', 'CNW'), ('F04', 'CSE'), ('F05', 'CSE'), ('F13', 'CSW'), ('F18', 'CSE'), ('F20', 'CSW'), ('F24', 'CSE'), ('F32', 'CNW'), ('F38', 'CNW'), ('F40', 'CNE')], _group='temp', _domain=(0, 120))

	s += d.get_bms_series("345---------001BMSELEMET------VAL001", _from, _to, _group='electric', _domain=(0, 1500))
	s += d.get_bms_series("345---------001BMSSTEMET------VAL001", _from, _to, _group='steam')
	s += d.get_bms_series("345---------000SECCNTPEOBUI---VAL001", _from, _to, _group='occupancy')

	d2 = DatabaseInterface("anderson.ldeo.columbia.edu", "Weather", "Hooshmand", "Breakit68")
	s += d2.get_generic_series(("Observations_History", "Weather"), "Date", [("TempA", "Temp"), ("DewPointA", "DewPoint"), ("Humidity", "Humidity")], _from, _to, _group='weather')

	df = DataFrame()
	df.add_series(s)
	df.refine("occupancy", ["weather", "time"])

	mrt = MarkovRandomizedTree(df)
	
	mrt.addDependency('time', 'time')
	#mrt.addDependency('fan', ['fan', 'time', 'weather'])
	#mrt.addDependency('reheat', ['reheat', 'time', 'weather'])
	#mrt.addDependency('pump', ['pump', 'time', 'weather'])
	mrt.addDependency('pumpsm', ['pumpsm', 'time', 'weather'])
	#mrt.addDependency('setpoint', ['setpoint', 'time'])

	mrt.addDependency('occupancy', ['occupancy', 'time', 'weather'])

	mrt.addDependency('electric', ['electric', 'occupancy', 'fan', 'time'])
	mrt.addDependency('steam', ['steam', 'pump', 'pumpsm', 'time'])
	mrt.addDependency('temp', ['temp', 'weather', 'fan', 'pump', 'steam', 'time'])
	mrt.addDependency('weather', ['weather', 'time'])


	form = "%Y-%m-%d"
	_from = dt.datetime.strptime(_from, form)
	_to = dt.datetime.strptime(_to, form+" %H:%M:%S")	
	#_to -= dt.timedelta(0, 5*60)

	###########


	ndf = df.subset(_from, _to)
	_before = str(_to + dt.timedelta(1))[:19]
	t = d2.get_forecast_series(("Hourly_Forecast", "Weather"), "Fcst_date", "Date", [("TempA", "Temp"), ("DewA", "DewPoint"), ("Humidity", "Humidity")], _to, _before, _group='weather')
	#odf = DataFrame()
	#odf.add_series(t)
	#forecast_from = str(ndf.timestamps[-1] - dt.timedelta(0, 15*60))[:19]
	#forecast_from = str(ndf.timestamps[-1])[:19]
	#forecast_to = str(odf.timestamps[-1])[:19]

	forecast_from = _to - dt.timedelta(7)
	forecast_to = _to + dt.timedelta(1, 12 * 3600) 

	t += d.get_bms_series("345---------001BMSHVAFANLCP---VAL001", forecast_from, forecast_to, _group='fan', _discrete=True, last=True)
	#t += d.get_bms_series("345---------001BMSHVAFANRHC---SPV001", forecast_from, forecast_to, _group='reheat', _discrete=True)
	t += d.get_bms_series("345---------001BMSWATSECPUM---VAL001", forecast_from, forecast_to, _group='pump', _discrete=True, last=True)
	#t += d.get_bms_series("345---------001BMSWATSECSMO---VAL001", forecast_from, forecast_to, _group='pumpsm', _discrete=True)

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

	###########

	bestPDF = None

	c = {}
	for pointname in df.pointnames:
		c[pointname] = numpy.floor(numpy.random.rand(3) * 5)/5

	groups = ['occupancy', 'electric', 'steam', 'temp']
	unitsm = ['Occupancy', 'Electric Load ($kW$)', 'Steam Demand ($Mlb$/$h$)', 'Temperatrue ($^{\circ}F$)']
	titles = ['Occupancy', 'Electric Consumption', 'Steam Demand', 'Interior Space Temperature']
	for group, unitm, title in zip(groups, unitsm, titles):
			
		fig, ax = plt.subplots()

		for x, name, i in zip(df.X.T, df.pointnames, xrange(df.covarSize)):
			if not(i in df.group[group]):
				continue
			_c = None
			try:
				_c = c[name]
			except:
				_c = numpy.random.rand(3)
		
			#ax.plot(df.timestamps, x, color=_c)
			ax.plot(df.timestamps, x, color='blue')

		for pdf, _c1 in zip(PDF, costs):
			#_c1 = numpy.random.rand(3)
			if _c1 == 0:
				bestPDF = pdf
			for x, name, i in zip(pdf.X.T, pdf.pointnames, xrange(pdf.covarSize)):
				if not(i in pdf.group[group]):
					continue
				_c = None
				try:
					_c = c[name]
				except:
					_c = numpy.random.rand(3)

				if _c1 == 0:
					ax.plot(pdf.timestamps, x, '-o', color='green')

				else:
					ax.plot(pdf.timestamps, x, '--', color=numpy.array([_c1, 0, 1-_c1]))

		plt.xlabel('time')
		plt.ylabel(unitm)
		plt.title(title)
		
	#plt.show()
	#bestPDF.plot()

	output_table = {}
	output_table['fan'] = '345---------001TPOHVAFANLCP---VAL001'
	output_table['pump'] = '345---------001TPOWATSECPUM---VAL001' 

	now = str(dt.datetime.now())[:19]
	
	for g in ['fan', 'pump']:
		for i in bestPDF.group[g]:
			table = output_table[g]
			d.commit_bms_series(table, now, bestPDF.pointnames[i], bestPDF.timestamps, bestPDF.X.T[i])


if __name__ == '__main__':
	#test('2014-08-01', '2014-11-07 01:00:00')
	now = str(dt.datetime.now())[:19]
	#search('2014-01-01', '2014-11-07 01:00:00')
	search('2014-01-01', now)
	#f = open("model.txt", 'rb')
	#mrt = pickle.load(f)

