
import pyodbc
import datetime as dt
import scipy
import sklearn.ensemble
import numpy
import scipy
import cfgparse

def absolute(timestamp, reference):
	dif = timestamp - reference
	return dif.days * 24 * 60 + dif.seconds / 60

def covariate(config_file, config_key):

	cparser = cfgparse.ConfigParser()

	cparser.add_option('building_db_server', dest='server', type='string', keys=config_key)
	cparser.add_option('building_db', dest='database', type='string', keys=config_key)
	cparser.add_option('db_user', dest='uid', type='string', keys=config_key)
	cparser.add_option('db_pwd', dest='pwd', type='string', keys=config_key)
	cparser.add_option('building_floors', dest='floors', type='string', keys=config_key)
	cparser.add_option('floor_quadrants', dest='quadrants', type='string', keys=config_key)
	cparser.add_option('space_temp_tablename_format', dest='space_temp_table', type='string', keys=config_key)

	cparser.add_file(config_file)
	options = cparser.parse()

	Floors = options.floors.replace(' ', '').split(',')
	Quadrants = options.quadrants.replace(' ', '').split(',')


	connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(options.server, options.database, options.uid, options.pwd))

	cursor = connection.cursor()

	print "Creating Covariates from BMS tables..."

	tables = cursor.tables()
	Tables = {} 

	count = 0
	for table in tables:
		if "BMS" in str(table) and not("[" in str(table)):
			Tables[table[2]] = []

	void = []

	for table in Tables:

		query = "SELECT DISTINCT ZONE, FLOOR, QUADRANT, EQUIPMENT_NO FROM [{0}] WHERE TIMESTAMP > '{1}'".format(table, str(dt.datetime.now() - dt.timedelta(0, 3 * 3600))[:23])
		#print query
		cursor.execute(query)
		keys = cursor.fetchall()

		if len(keys) == 0:
			print "No data found for " + table + ", can not be incorporated in the covariate object"
			void.append(table)
		else:
			for key in keys:
				Tables[table].append((str(key.ZONE), str(key.FLOOR), str(key.QUADRANT), str(key.EQUIPMENT_NO)))

	for table in void:
		Tables.pop(table, None)

	# Creating Dataset:

	Dataset = {}

	for table in Tables:

		print "Reading data from " + table

		# keys contain individual keys pertaining to individual distinct time series
		keys = Tables[table]

		for key in keys:
			query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE ZONE = '{1}' AND FLOOR = '{2}' AND QUADRANT = '{3}' AND EQUIPMENT_NO = '{4}' AND TIMESTAMP > '{5}' ORDER BY TIMESTAMP"

			now = dt.datetime.now()
			now = dt.datetime(now.year, now.month, now.day, now.hour)
			reference = now - dt.timedelta(20)

			query = query.format(table, key[0], key[1], key[2], key[3], str(reference)[:23] )

			vector = {} 

			cursor.execute(query)
			entries = cursor.fetchall()
			print "Timeseries " + str(key) + ":" + str(len(entries)) + " datapoints retrieved"
			for e in entries:
				vector[absolute(e.TIMESTAMP, reference)] = e.VALUE

			Dataset["{0},{1},{2},{3},{4}".format(table, key[0], key[1], key[2], key[3])] = vector

	print "Dataset retrieved."
	
	matrix = []

	timestamp = set([])
	for t in Dataset:
		timestamp = timestamp.union(set(Dataset[t].keys()))

	timestamp = sorted(list(timestamp))
	timeseries = sorted(Dataset.keys())

	index = 0

	Ondex = []
	OndexName = []
	for series in timeseries:
		vector = []

		for i in range(0, len(Floors)):
			if options.space_temp_table in series and Floors[i] in series and Quadrants[i] in series:
				Ondex.append(index)
				OndexName.append(series)
		for stamp in timestamp:	
			dictionary = Dataset[series]
			try:
				vector.append(float(dictionary[stamp]))
			except:
				vector.append(-9999)
		matrix.append(vector)
		index += 1

	#adding the time of day feature
	time_feature = numpy.array(timestamp)
	time_feature = time_feature % (24 * 60)
	time_feature = list(time_feature)
	matrix.append(time_feature)

	transpose = []
	for j in range(0, len(matrix[0])):
		sample = []
		for i in range(0, len(matrix)):
			sample.append(matrix[i][j])
		transpose.append(sample)

	outputs = []
	for ondex in Ondex:
		outputs.append(matrix[ondex])

	#####
	corrupt_index = []
	for ondex in Ondex:
		count = 0
		for i in matrix[ondex]:
			if i == -9999 or i < 0 or i > 120:
				corrupt_index.append(count)

			count += 1

	valid_set = set(range(0, len(transpose)))
	valid_set = valid_set.difference(set(corrupt_index))
	Transpose = []
	Outputs = []

	for i in sorted(list(valid_set)):
		Transpose.append(transpose[i])
	for out in outputs:
		Out = []
		for i in sorted(list(valid_set)):
			Out.append(out[i])
		Outputs.append(Out)


	cursor.close()
	connection.close()

	print "Covariate matrix constructed."

	#return transpose, outputs
	return Transpose, Outputs, OndexName


def model(CovariateMatrix):

	print "Building models for short term forecast for individual floors..."

	ETR = sklearn.ensemble.ExtraTreesRegressor()

	X = CovariateMatrix[0]

	Y = CovariateMatrix[1]

	Name = CovariateMatrix[2]

	timestamps = [0, 15, 30, 45, 60, 75, 90, 105]
	
	F = []
	
	index = 0
	for y in Y:
		floor = []
		floor.append(y[-1])
		print "\t" + Name[index]
		for i in range(1, 8):
			print "\t" + str(timestamps[i]) + " minutes ahead..."
			ETR.fit(X[:-i], y[i:]) 
			floor.append(ETR.predict([X[-1]])[0])
		F.append(floor)
		index += 1

	print F 

	return F, Name

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

	Run_DateTime = str(dt.datetime.now())[:23]
	now = dt.datetime.now()
	Prediction_DateTime = dt.datetime(now.year, now.month, now.day, now.hour, now.minute/15 * 15)

	for i in range(0, len(Forecast)):
		count = 0
		for data in Forecast[i]:
			S = Series[i].split(',')
			Table = options.database+'---------000TPONOWTEMSPA001---001'
			Floor = S[2]
			Quadrant = S[3]

			query = "INSERT INTO [{0}] (Run_DateTime, Prediction_DateTime, Value, Floor, Quadrant) VALUES ('{1}', '{2}', {3}, '{4}', '{5}')"
			query = query.format(Table, Run_DateTime, str(Prediction_DateTime+dt.timedelta(0, count * 15 * 60))[:23], str(data), str(Floor), str(Quadrant))

			print query

			cursor.execute(query)
			cursor.commit()
			count += 1

	cursor.close()
	connection.close()


def forecast(config_file, config_key):

	X, Y, Name = covariate(config_file, config_key)

	F, Name = model([X, Y, Name])

	commit(F, Name, config_file, config_key)


forecast('C:\\Rudin\\config.ini', 'Rudin_345Park')
forecast('C:\\Rudin\\config.ini', 'Rudin_560Lexington')
forecast('C:\\Rudin\\config.ini', 'Rudin_40E52')
forecast('C:\\Rudin\\config.ini', 'Rudin_1BP')
forecast('C:\\Rudin\\config.ini', 'Rudin_641LE')
forecast('C:\\Rudin\\config.ini', 'Rudin_WHI')


