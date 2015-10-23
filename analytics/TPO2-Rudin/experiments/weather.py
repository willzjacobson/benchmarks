
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
	Metadata = []

	## Offset
	offset = dt.datetime.now() - dt.timedelta(off)
	offset = offset.date()
	offset = dt.datetime(offset.year, offset.month, offset.day)


	tables = []

	T = cursor.tables()
	for t in T:
		if ("BMS" in str(t[2]) or "SECCNTPEOBUI" in str(t[2])) and not("[" in str(t[2])):
			tables.append(str(t[2]))



	connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(options.server, options.database, options.uid, options.pwd))

	cursor = connection.cursor()

	print "Creating Covariates from BMS tables..."

	cursor.close()
	connection.close()
	# Terminating main database connection


	## Establishing connection to 345 database for feedback data
	connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format('anderson.ldeo.columbia.edu', '345', 'Hooshmand', 'Breakit68'))
	cursor = connection.cursor()


	query = "SELECT Actual_DateTime From [Score_Startup_Rampdown] WHERE Building = '{0}' AND Tag = '{1}' ORDER BY Actual_DateTime".format('345', 'startup')
	cursor.execute(query)
	entries = cursor.fetchall()

	x = []
	for entry in entries:
	
		x.append(entry.Actual_DateTime)

	Metadata.append(x)

	query = "SELECT Actual_DateTime From [Score_Startup_Rampdown] WHERE Building = '{0}' AND Tag = '{1}' ORDER BY Actual_DateTime".format('345', 'rampdown')
	cursor.execute(query)
	entries = cursor.fetchall()

	x = []
	for entry in entries:
	
		x.append(entry.Actual_DateTime)


	Metadata.append(x)

	cursor.close()
	connection.close()
	# Terminating database connection

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

	Dataset.append([timestamp, value])
	## Terminating weather database connection

	print "Covariate matrix constructed."
	return Dataset, Metadata


def model(CovariateMatrix, meta):

	print "Building models for short term forecast for individual floors..."

	#for z in CovariateMatrix:

	pre = ExtraTreesRegressor()	

	fig, ax = plt.subplots()

	timestamps = set([])
	_CovariateMatrix = []

	action = [] 
	for i in meta[0]:
		if i == None:
			continue
		action.append(i)
	startup = {}
	for i in action:
		startup[dt.datetime(i.year, i.month, i.day)] = i.hour*60 + i.minute

	for z in CovariateMatrix:
		[x, y] = z

		_x = []
		_y = []

		for i in range(0, len(x)):
			if y[i] < -100:
				continue

			_x.append(dt.datetime(x[i].year, x[i].month, x[i].day, x[i].hour, x[i].minute))
			_y.append(y[i])

		_CovariateMatrix.append([_x, _y])

		#ax.plot(x, y, color='blue')



	avg = {}

	for z in _CovariateMatrix:
		[x, y] = z	

		for i in range(0, len(x)):
			current = dt.datetime(x[i].year, x[i].month, x[i].day, 12)

			try:
				avg[current].append(y[i])
			except:
				avg[current] = []

		#ax.plot(x, y, color='red')	

	x = []
	y = []
	for t in sorted(avg.keys()):
		x.append(t)
		y.append(sum(avg[t])/len(avg[t]))

	#ax.plot(x, y, color='purple')

	#########
	[_x, _y] = _CovariateMatrix[0]

	x = []
	y = []

	clist = ['', 'purple', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red']

	current  = dt.datetime(_x[0].year, _x[0].month, _x[0].day) + dt.timedelta(1)
	for i in range(0, len(_x)):
		if _x[i] > current:
			flag = 0
			try:
				s = startup[current - dt.timedelta(1)]
				if  s >= 360 and s < 465:
					print current - dt.timedelta(1)
					flag = int((s - 360) / 15) + 1
					#flag = 1
			except:
				flag = 0 

			if flag:
				z = y[len(y)/4:len(y)/2]
				ax.scatter(flag, [sum(z)/len(z)], color=clist[flag])
			x = []
			y = []
			current += dt.timedelta(1)

		x.append(_x[i].hour * 60 + _x[i].minute)
		y.append(_y[i])

	#ax.hist(startup.values(), bins=1000)

	plt.show()

	#########

	#fig, ax = plt.subplots()
	#ax.plot(x, y)	
	#ax.scatter(x, y, color='blue')
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


def forecast(config_file, config_key):

	X, meta = covariate(config_file, config_key, 200)
	model(X, meta)

	#commit(F, Name, config_file, config_key)





forecast('C:\\Rudin\\config_master.json', 'Rudin_345Park')
#forecast('C:\\Rudin\\config_master.json', 'Rudin_560Lexington')
#forecast('C:\\Rudin\\config_master.json', 'Rudin_40E52')
#forecast('C:\\Rudin\\config_master.json', 'Rudin_1BP')
#forecast('C:\\Rudin\\config_master.json', 'Rudin_641LE')
#forecast('C:\\Rudin\\config_master.json', 'Rudin_WHI')


