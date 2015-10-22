
import pyodbc
import datetime as dt
import scipy
import sklearn.ensemble
import numpy
import scipy
import cfgparse
import matplotlib.pyplot as plt 

import math

from sklearn.cluster import KMeans
from sklearn import cluster
from sklearn import linear_model
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import ExtraTreesClassifier

def absolute(timestamp, reference):
	dif = timestamp - reference
	return dif.days * 24 * 60 + dif.seconds / 60

def covariate(config_file, config_key, off):

	cparser = cfgparse.ConfigParser()
	wcparser = cfgparse.ConfigParser()

	cparser.add_option('building_db_server', dest='server', type='string', keys=config_key)
	cparser.add_option('building_db', dest='database', type='string', keys=config_key)
	cparser.add_option('db_user', dest='uid', type='string', keys=config_key)
	cparser.add_option('db_pwd', dest='pwd', type='string', keys=config_key)
	cparser.add_option('building_floors', dest='floors', type='string', keys=config_key)
	cparser.add_option('floor_quadrants', dest='quadrants', type='string', keys=config_key)
	cparser.add_option('space_temp_tablename_format', dest='space_temp_table', type='string', keys=config_key)
	cparser.add_option('electric_load_table', dest='electric_table', type='string', keys=config_key)

	'''
	cparser.add_options('', dest='', type='string', key=config_key)
	cparser.add_options('', dest='', type='string', key=config_key)
	cparser.add_options('', dest='', type='string', key=config_key)
	cparser.add_options('', dest='', type='string', key=config_key)
	'''

	cparser.add_option('weather_station_id', dest='weather_config', type='string', keys=config_key)

	cparser.add_file(config_file)
	options = cparser.parse()

	Floors = options.floors.replace(' ', '').split(',')
	Quadrants = options.quadrants.replace(' ', '').split(',')

	# Weather station config parser
	wcparser.add_option('weather_db', dest='database', type='string', keys=options.weather_config)
	wcparser.add_option('weather_db_server', dest='server', type='string', keys=options.weather_config)
	wcparser.add_option('weather_db_user', dest='user', type='string', keys=options.weather_config)
	wcparser.add_option('weather_db_pwd', dest='pwd', type='string', keys=options.weather_config)
	wcparser.add_option('weather_table', dest='table', type='string', keys=options.weather_config)
	
	wcparser.add_file(config_file)
	woptions = wcparser.parse()
	# Weather stating config parser constructed

	## Establishing connection
	connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(options.server, options.database, options.uid, options.pwd))

	cursor = connection.cursor()

	Dataset = [] 
	Title = []

	## Offset
	offset = dt.datetime.now() - dt.timedelta(off)
	offset = offset.date()
	offset = dt.datetime(offset.year, offset.month, offset.day)

	#tables = [options.space_temp_table, options.electric_table]
	#tables = [options.space_temp_table, 'WHI---------006BMSHVASFASAT---STA001']
	#tables = [options.space_temp_table] 
	#tables = ['WHI---------006BMSHVASFASAT---STA001']
	tables = []

	T = cursor.tables()
	for t in T:
		if ("BMS" in str(t[2]) or "SECCNTPEOBUI" in str(t[2])) and not("[" in str(t[2])):
			tables.append(str(t[2]))

	#tables = [options.space_temp_table] 

	## Retrieve space temperature
	for table in tables:
		print table
		query = "SELECT DISTINCT ZONE, FLOOR, QUADRANT, EQUIPMENT_NO FROM [{0}]".format(table)
		cursor.execute(query)
		entries = cursor.fetchall()

		Keys = []
		for e in entries:
			Keys.append((e.ZONE, e.FLOOR, e.QUADRANT, e.EQUIPMENT_NO))

		for key in Keys:
			query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE ZONE = '{1}' AND FLOOR = '{2}' AND QUADRANT = '{3}' AND EQUIPMENT_NO = '{4}' AND TIMESTAMP > '{5}' ORDER BY TIMESTAMP"
			query = query.format(table, key[0], key[1], key[2], key[3], str(offset))


			cursor.execute(query)
			entries = cursor.fetchall()
			print str(key) + ': ' + str(len(entries))
		
			timestamp = []
			value = []

			for e in entries:
				#if e.VALUE > 100 or e.VALUE <= 0:
				#	continue
				timestamp.append(e.TIMESTAMP)
				value.append(e.VALUE)

			Dataset.append([timestamp, value])
			Title.append(str(table)+','+str(key[0])+','+str(key[1])+','+str(key[2])+','+str(key[3]))


	connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(options.server, options.database, options.uid, options.pwd))

	cursor = connection.cursor()

	print "Creating Covariates from BMS tables..."


	cursor.close()
	connection.close()
	# Terminating main database connection

	## Establishing weather database connection
	connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(woptions.server, woptions.database, woptions.user, woptions.pwd))

	cursor = connection.cursor()

	query = "SELECT * FROM [{0}] WHERE Date > '{1}' ORDER BY Date".format(woptions.table, str(offset))

	cursor.execute(query)
	entries = cursor.fetchall()

	print woptions.table + ": " + str(len(entries))

	timestamp = []
	value = []
	for e in entries:
		ts = dt.datetime.strptime(str(e.Date)[:19], '%Y-%m-%d %H:%M:%S')
		timestamp.append(ts)
		value.append(e.TempA)

	#Dataset.append([timestamp, value])
	## Terminating weather database connection

	print "Covariate matrix constructed."
	return Dataset, Title


def matrix(CovariateMatrix, Title):

	timestamps = set([])
	_CovariateMatrix = []

	for z in CovariateMatrix:
		[x, y] = z

		_x = []
		_y = []

		for i in range(0, len(x)):
			_x.append(dt.datetime(x[i].year, x[i].month, x[i].day, x[i].hour, x[i].minute))
			_y.append(y[i])

		_CovariateMatrix.append([_x, _y])


	s = []
	e = []

	_counter = 0
	for z in _CovariateMatrix:
		[x, y] = z

		a = []

		#ax.plot(x, y, color='blue')
		if y != []:

			for j in range(1, len(y)):
				a.append(y[j] - y[j-1])


			fig1, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
			ax1.set_ylabel('Measurement')
			ax2.set_ylabel('Anomoly Score')
			ax2.set_xlabel('Timestamp')

			ax1.set_title(Title[_counter])

			'''
			fig3, ax3 = plt.subplots()
			ax3.set_xlabel('Anomoly Score')
			ax3.set_ylabel('Observations')

			fig4, ax4 = plt.subplots()
			ax4.set_xlabel('Timestamp')
			ax4.set_ylabel('Measurement')

			ax3.set_title(Title[_counter])
			ax4.set_title(Title[_counter])

			'''

			v = []
			w = []

			for index in range(0, len(y)-20):
				v.append(y[index])
				w.append(y[index+20])


			ax1.plot(x, y)

			#ax4.plot(x, y)

			for window in numpy.arange(50, 60, 20):
				for length in numpy.arange(5, window, 2):
					delta = distance(x, y, window, length)
					ax2.plot(x[window:-window], delta)
			#ax3.hist(v, bins=30)

			w = []
			for i in range(1, len(y)):
				w.append(y[i] - y[i-1])

			#fig3, ax3 = plt.subplots()
			#ax3.plot(x[1:], w, color='red')	

			q = []

			window = 10
			for i in range(0, len(y))[window:-window]:

				q.append(0)
				for pointer in range(-window, window + 1):
					q[-1] += y[i + pointer]
			#fig4, ax4 = plt.subplots()
			#ax2.plot(x[window:-window], q, color='green')
			plt.show()


		_counter += 1

		if x == []:
			continue

		s.append(x[0])
		e.append(x[-1])


	S = min(s)
	E = max(e)

	while S.minute % 15 != 0:
		S += dt.timedelta(0, 60)
		
	while S.minute % 15 != 0:
		E -= dt.timedelta(0, 60)

	timestamp = {}

	current = S 
	while current <= E:
		timestamp[current] = []
		current += dt.timedelta(0, 15 * 60)

	covariate = 0
	for z in _CovariateMatrix:

		covariate += 1
		[x, y] = z

		for i in range(0, len(x)):
				
			try:
				if len(timestamp[x[i]]) == covariate - 1:
					timestamp[x[i]].append(y[i])
			except:
				continue

		for t in timestamp:
			if len(timestamp[t]) != covariate:
				timestamp[t].append(-9999)


	x = sorted(timestamp.keys()) 
	Y = []
	for i in range(0, len(timestamp[x[0]])):
		Y.append([])
	for t in x:
		for i in range(0, len(timestamp[t])):
			Y[i].append(timestamp[t][i])

	for i in range(0, len(Y)):

		total = 0
		count = 0
		indices = []
		temp = []

		for j in range(0, len(Y[i])):
			if Y[i][j] < 0:
				continue
			try:
				if Y[i][j] == Y[i][j-1]:
					temp.append(j)
					count += 1
					total += 1

				elif count > 8 * 4:
					indices += temp
					temp = []
					count = 0
				else:
					count = 0
					temp = []

			except:
				continue


		#for j in indices:
		#	Y[i][j] = -9999


		#ax.plot(x, Y[i], color='red')

	#plt.show()


	return x, Y


def reconstruct(Times, Title, Matrix, config_file, config_key):

	X = []

	cov = []
	learn = {} 
	test = {} 

	cparser = cfgparse.ConfigParser()
	cparser.add_option('occupancy_table', dest='occupancy_table', type='string', keys=config_key)
	cparser.add_file(config_file)
	options = cparser.parse()

	print "Reconstructing the dataset..."

	fig, ax = plt.subplots()
	index = 0
	for c in range(0, len(Matrix)):

		print Title[index]
		index += 1

		X = []
		y = []
		_X = []
		I = []
		for i in range(0, len(Times)):
			t = Times[i]
			if Matrix[c][i] >= 0:
				X.append([t.hour * 60 + t.minute, t.weekday()])
				y.append(Matrix[c][i])
			else:
				_X.append([t.hour * 60 + t.minute, t.weekday()])
				I.append(i)

		if X == [] or _X == []:
			continue

		pre = ExtraTreesRegressor()
		pre.fit(X, y)
		_y = pre.predict(_X)

		count = 0
		for i in I:
			Matrix[c][i] = _y[count]
			count += 1

		ax.plot(Times, Matrix[c])

	#plt.show()

	return Matrix

def model(Matrix, Times, Title, config_file, config_key):

	print "Building models for short term forecast for individual floors..."

	cparser = cfgparse.ConfigParser()

	cparser.add_option('space_temp_tablename_format', dest='space_temp_table', type='string', keys=config_key)
	cparser.add_option('electric_load_table', dest='electric_table', type='string', keys=config_key)
	cparser.add_option('occupancy_table', dest='occupancy_table', type='string', keys=config_key)
	cparser.add_option('fan_table', dest='fan_table', type='string', keys=config_key)

	cparser.add_option('building_open_hour', dest='lease_open', type='int', keys=config_key)

	cparser.add_option('weather_station_id', dest='weather_config', type='string', keys=config_key)

	cparser.add_file(config_file)
	options = cparser.parse()


	# Building dataset


	fig, ax = plt.subplots()

	X = []
		
	for j in range(0, len(Matrix[0])):
		x = []
		for i in range(0, len(Matrix)):
			x.append(Matrix[i][j])
		X.append(x)

	for i in range(0, len(Times)):
		X[i].append(Times[i].weekday())
		X[i].append(Times[i].hour * 60 + Times[i].minute)


	y = []
	x = []
	w = []
	z = []

	for i in range(0, len(Matrix)):
		if options.fan_table in Title[i]:
			ax.plot(Times, Matrix[i])

			for j in range(1, len(Matrix[i])):
				if Matrix[i][j] != Matrix[i][j-1]:

					if Matrix[i][j] > Matrix[i][j-1]:
						x.append(Times[j])
						y.append(3)
						continue

					if Matrix[i][j] < Matrix[i][j-1]:

						w.append(Times[j])
						z.append(2)


		if options.space_temp_table in Title[i]:
			ax.plot(Times, Matrix[i])


	ax.scatter(x, y, color='red')
	ax.scatter(w, z, color='blue')

	#plt.show()


def commit(Forecast, Series, config_file, config_key):
	
	print "Predictions were made."
	print "Commiting forecasts..."

	cparser = cfgparse.ConfigParser()

	cparser.add_option('results_db_server', dest='server', type='string', keys=config_key)
	cparser.add_option('results_db', dest='database', type='string', keys=config_key)
	cparser.add_option('results_db_user', dest='uid', type='string', keys=config_key)
	cparser.add_option('results_db_pwd', dest='pwd', type='string', keys=config_key)

	cparser.add_file(config_file)
	options = cparser.parse()
	connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(options.server, options.database, options.uid, options.pwd))

	cursor = connection.cursor()

	cursor.close()
	connection.close()

def distance(x, y, window, sequence_length, sequence=False):

	delta = []
	for i in range(0 + window, len(x) - window):
		dist = 0
		for j in range(-window, window + 1):
			for k in range(-sequence_length, sequence_length + 1):
				dist += abs(y[i + k] - y[j + k])
		delta.append(dist)

	delta = numpy.array(delta)/(window * sequence_length)
	return delta

def forecast(config_file, config_key):

	C, Title = covariate(config_file, config_key, 7)

	Times, X = matrix(C, Title)

	Matrix = reconstruct(Times, Title, X, config_file, config_key)	

	model(Matrix, Times, Title, config_file, config_key)

	#commit(F, Name, config_file, config_key)



forecast('C:\\Rudin\\config.ini', 'Rudin_345Park')
forecast('C:\\Rudin\\config.ini', 'Rudin_560Lexington')
forecast('C:\\Rudin\\config.ini', 'Rudin_40E52')
forecast('C:\\Rudin\\config.ini', 'Rudin_1BP')
forecast('C:\\Rudin\\config.ini', 'Rudin_641LE')
forecast('C:\\Rudin\\config.ini', 'Rudin_WHI')


