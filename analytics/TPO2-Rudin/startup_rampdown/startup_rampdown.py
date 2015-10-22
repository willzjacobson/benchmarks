
import pyodbc
import datetime as dt
import datetime as DT
import scipy
import numpy
import scipy
import cfgparse
import optparse

import math
import random

import sklearn.ensemble
from sklearn.ensemble import ExtraTreesClassifier
from scipy import interpolate

import sys, os

from common_rudin.common import log_from_config, setup, setup_cparser

__version__ = "$ID"
__author__ = "hs2703@columbia.edu"
_module = "Recommendation"


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
	cparser.add_option('steam_demand_table', dest='steam_table', type='string', keys=config_key)
	cparser.add_option('space_temp_tablename_format', dest='space_temp_table', type='string', keys=config_key)
	cparser.add_option('electric_load_table', dest='electric_table', type='string', keys=config_key)
	cparser.add_option('occupancy_table', dest='occupancy_table', type='string', keys=config_key)

	cparser.add_option('has_steam_supply', dest='has_steam', type='int', keys=config_key)
	
	cparser.add_option('results_table_steam', dest='results_steam', type='string', keys=config_key)
	cparser.add_option('results_table', dest='results_temp', type='string', keys=config_key)
	cparser.add_option('results_table_electric', dest='results_electric', type='string', keys=config_key)
	cparser.add_option('results_table_occupancy', dest='results_occupancy', type='string', keys=config_key)

	cparser.add_option('fan_table', dest='fan_table', type='string', keys=config_key)	

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
	wcparser.add_option('weather_table', dest='weather_table', type='string', keys=options.weather_config)
	wcparser.add_option('weather_forecast_table', dest='forecast_table', type='string', keys=options.weather_config)

	
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


	results = [options.results_occupancy, options.results_electric]
	tables = [options.occupancy_table, options.electric_table]

	if options.has_steam:
		results.append(options.results_steam)
		tables.append(options.steam_table)

	
	print "Retrieving forecast data"
	for i in range(0, len(results)):
		query = "SELECT * FROM ([{0}] a INNER JOIN (SELECT MAX(Run_DateTime) as most_recent FROM [{1}]) b ON a.Run_DateTime = b.most_recent) ORDER BY Prediction_DateTime" 
		query = query.format(results[i], results[i])
		cursor.execute(query)
		entries = cursor.fetchall()

		row = []

		x = []
		y = []

		row.append([x, y])

		for e in entries:
			x.append(e.Prediction_DateTime)
			y.append(e.Prediction_Value) 
			#print "{0}: {1}".format(results[i], str(e.Prediction_DateTime))

		query = "SELECT DISTINCT ZONE, FLOOR, QUADRANT, EQUIPMENT_NO FROM [{0}] WHERE TIMESTAMP > '{1}'"
		query = query.format(tables[i], str(offset)[:10])
		cursor.execute(query)
		point_name_list = cursor.fetchall()

		t = []
		T = {}

		for point_name in point_name_list:
			query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE ZONE='{1}' AND FLOOR='{2}' AND QUADRANT='{3}' AND EQUIPMENT_NO='{4}' AND TIMESTAMP >'{5}' ORDER BY TIMESTAMP"
			query = query.format(tables[i], point_name.ZONE, point_name.FLOOR, point_name.QUADRANT, point_name.EQUIPMENT_NO, str(offset)[:10])
			cursor.execute(query)
			entries = cursor.fetchall()

			t.append({})

			for e in entries:
				t[-1][e.TIMESTAMP] = e.VALUE
				#if len(tables[i]) == 36:
				#	print "{0}{1}{2}{3}{4}{5}{6}: {7}".format(tables[i][:3], point_name.ZONE, point_name.FLOOR, point_name.QUADRANT, tables[i][3+9:12+15], point_name.EQUIPMENT_NO, tables[i][12+15+3:], str(e.TIMESTAMP))
				#else:
				#	print "{0}: {1}".format(tables[i], str(e.TIMESTAMP))

		for d in t:
			for timestamp in d:
				try:
					T[timestamp] += d[timestamp]
				except:
					T[timestamp] = d[timestamp]

		x = []
		y = []
		row.append([x, y])
		for datetimes in sorted(T.keys()):
			x.append(datetimes)
			y.append(T[datetimes])



		Dataset.append(row)
	
	table = options.results_temp


	for i in range(0, len(Floors)):
		query = "SELECT * FROM ([{0}] a INNER JOIN (SELECT MAX(Run_DateTime) as most_recent FROM [{1}]) b ON a.Run_DateTime = b.most_recent) WHERE Floor = '{2}' AND Quadrant = '{3}'  ORDER BY Prediction_DateTime" 
		query = query.format(table, table, Floors[i], Quadrants[i])
		cursor.execute(query)
		entries = cursor.fetchall()

		row = []

		x = []
		y = []
		for e in entries:
			x.append(e.Prediction_DateTime)
			y.append(e.Prediction_Value)

		row.append([x, y])

		query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE TIMESTAMP > '{1}' AND FLOOR = '{2}' AND QUADRANT = '{3}' ORDER BY TIMESTAMP"
		query = query.format(options.space_temp_table, str(offset)[:10], Floors[i], Quadrants[i])
		cursor.execute(query)
		entries = cursor.fetchall()

		x = []
		y = []

		row.append([x, y])

		for e in entries:
			x.append(e.TIMESTAMP)
			y.append(e.VALUE)	

		Dataset.append(row)

	fan_data = []
	query = "SELECT DISTINCT ZONE, FLOOR, QUADRANT, EQUIPMENT_NO FROM [{0}] WHERE TIMESTAMP > '{1}'"
	query = query.format(options.fan_table, str(offset)[:20])
	cursor.execute(query)
	point_name_list = cursor.fetchall()

	for point_name in point_name_list:
		query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE TIMESTAMP > '{1}' AND ZONE='{2}' AND FLOOR='{3}' AND QUADRANT='{4}' AND EQUIPMENT_NO='{5}' ORDER BY TIMESTAMP"
		query = query.format(options.fan_table, str(offset)[:20], point_name.ZONE, point_name.FLOOR, point_name.QUADRANT, point_name.EQUIPMENT_NO)

		cursor.execute(query)
		entries = cursor.fetchall()

		x = []
		y = []
		for e in entries:
			x.append(e.TIMESTAMP)
			y.append(e.VALUE)

		fan_data.append([x, y])

	# Gathering Occupancy Data
	query = "SELECT * FROM ([{0}] a INNER JOIN (SELECT MAX(Run_DateTime) as most_recent FROM [{1}]) b ON a.Run_DateTime = b.most_recent) ORDER BY Prediction_DateTime" 
	query = query.format(options.results_occupancy, options.results_occupancy)
	#query = query.format(options.results_electric, options.results_electric)
	cursor.execute(query)
	entries = cursor.fetchall()

	x = []
	y = []
	for e in entries:
		x.append(e.Prediction_DateTime)
		y.append(e.Prediction_Value)
	Occupancy_TimeSeries = [x, y]

	## collecting actual decisions
	actual_startups = []
	actual_rampdowns = []
	query = "SELECT * FROM Score_Startup_Rampdown WHERE Building = '{0}' AND Tag = 'startup' AND Actual_DateTime > '{1}' ORDER BY Actual_DateTime"
	query = query.format(options.database, str(offset)[:19])
	cursor.execute(query)
	entries = cursor.fetchall()
	for e in entries:
		actual_startups.append(e.Actual_DateTime)
	query = "SELECT * FROM Score_Startup_Rampdown WHERE Building = '{0}' and Tag = 'rampdown' AND Actual_DateTime > '{1}' ORDER BY Actual_DateTime"
	query = query.format(options.database, str(offset)[:19])
	cursor.execute(query)
	entries = cursor.fetchall()
	for e in entries:
		actual_rampdowns.append(e.Actual_DateTime)

	cursor.close()
	connection.close()

	## Establishing connection
	connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(woptions.server, woptions.database, woptions.user, woptions.pwd))
	cursor = connection.cursor()


	query = "SELECT * FROM ([{0}] a INNER JOIN (SELECT MAX(Fcst_date) as most_recent FROM [{1}]) b ON a.Fcst_date = b.most_recent) ORDER BY Date"
	query = query.format(woptions.forecast_table, woptions.forecast_table)

	cursor.execute(query)
	entries = cursor.fetchall()

	row = []
	x = []
	y = []
	row.append([x, y])
	for e in entries:
		ts = str(e.Date)[:16]
		ts = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M")
		x.append(ts)
		y.append(e.TempA)

	query = "SELECT * FROM [{0}] WHERE Date > '{1}' ORDER BY Date"
	query = query.format(woptions.weather_table, str(offset)[:10])
	cursor.execute(query)
	entries = cursor.fetchall()

	x = []
	y = []
	row.append([x, y])
	for e in entries:
		ts = str(e.Date)[:16]
		ts = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M")
		x.append(ts)
		y.append(e.TempA)


	Dataset.append(row)

	Dataset.append(fan_data)

	cursor.close()
	connection.close()

	print "Covariate matrix constructed."
	#return Dataset, Title
	return Dataset, Occupancy_TimeSeries, [actual_startups, actual_rampdowns]


def recommend_action(Dataset, Occupancy_TimeSeries, actuals, logger):

	print "Building covariate matrix..."

	fan_data = Dataset.pop()

	datetimes = []
	for point_name in Dataset:
		[forecast, actual] = point_name
		for timestamp in actual[0]:
			datetimes.append(timestamp)
	datetimes = sorted(list(set(datetimes)))	

	offset_minutes = []
	base = datetimes[0]
	for dt in datetimes:
		offset = dt - base
		offset_minutes.append(offset.days * 24 * 60 + offset.seconds/60)

	datetime_index = {}
	index = 0
	for dt in datetimes:
		datetime_index[dt] = index
		index += 1

	matrix = []		
	for point_name in Dataset:

		matrix.append([])
		for dt in datetimes:
			matrix[-1].append(-1)


		[forecast, actual] = point_name

		[x, y] = actual				

		for i in range(0, len(x)):
			matrix[-1][datetime_index[x[i]]] = y[i]

		[x, y] = forecast

	for i in range(0, len(matrix)):
		gap_x = []
		gap_i = []
		available_x = []
		available_y = []
		for j in range(0, len(matrix[i])):
			if matrix[i][j] == -1:
				gap_x.append(offset_minutes[j])
				gap_i.append(j)
			else:
				available_x.append(offset_minutes[j])
				available_y.append(matrix[i][j])

		if gap_x != [] and available_x != []:
			gap_y = numpy.interp(gap_x, available_x, available_y)
			for j in range(0, len(gap_i)):
				matrix[i][gap_i[j]] = gap_y[j]


	train_datetimes = datetimes
	train_matrix = matrix

	fan_estimators = []

	print "Building models for fan predictions..."
	for single_fan in fan_data:

		[x, y] = single_fan

		X = []
		Y = []
		for i in range(0, len(x)):
			try:
				index = datetime_index[x[i]]
				Y.append(y[i])
				point = []
				for point_name in range(0, len(matrix)):
					point.append(matrix[point_name][index])
				point.append(datetimes[index].hour * 60 + datetimes[index].minute)
				point.append(datetimes[index].weekday())
				X.append(point)	
			except:
				continue

		if X != []:	

			best_model = None 
			best_score = 0
			for tries in xrange(10):
				#cross validating
				pre = ExtraTreesClassifier()
				data_size = len(X)
				train_indices = random.sample(xrange(data_size), int(0.9 * data_size))
				test_indices = list(set(xrange(data_size)).difference(set(train_indices)))
				train_X = [X[i] for i in train_indices]
				train_Y = [Y[i] for i in train_indices]
				test_X = [X[i] for i in test_indices]
				test_Y = [Y[i] for i in test_indices]
				pre.fit(train_X, train_Y)
				score = pre.score(test_X, test_Y)
				if score > best_score:
					best_model = pre

			fan_estimators.append(best_model)

	#################

	datetimes = []
	for point_name in Dataset:
		[forecast, actual] = point_name
		for timestamp in forecast[0]:
			datetimes.append(timestamp)
	datetimes = sorted(list(set(datetimes)))

	dense_datetimes = []
	pointer_dt = datetimes[0]
	while pointer_dt <= datetimes[-1]:
		dense_datetimes.append(pointer_dt)
		pointer_dt = pointer_dt + DT.timedelta(0, 60)

	datetimes = sorted(list(set(dense_datetimes)))

	offset_minutes = []
	base = datetimes[0]
	for dt in datetimes:
		offset = dt - base
		offset_minutes.append(offset.days * 24 * 60 + offset.seconds/60)

	datetime_index = {}
	index = 0
	for dt in datetimes:
		datetime_index[dt] = index
		index += 1

	matrix = []		
	for point_name in Dataset:

		matrix.append([])
		for dt in datetimes:
			matrix[-1].append(-1)


		[forecast, actual] = point_name

		[x, y] = forecast 

		for i in range(0, len(x)):
			matrix[-1][datetime_index[x[i]]] = y[i]

		[x, y] = forecast

	

	for i in range(0, len(matrix)):
		gap_x = []
		gap_i = []
		available_x = []
		available_y = []
		for j in range(0, len(matrix[i])):
			if matrix[i][j] == -1:
				gap_x.append(offset_minutes[j])
				gap_i.append(j)
			else:
				available_x.append(offset_minutes[j])
				available_y.append(matrix[i][j])

		if gap_x != [] and available_x != []:
			gap_y = numpy.interp(gap_x, available_x, available_y)
			for j in range(0, len(gap_i)):
				matrix[i][gap_i[j]] = gap_y[j]

	X = []
	for row in matrix:
		for i in range(0, len(row)):
			try:
				X[i].append(row[i])
			except:
				X.append([])
				X[i].append(row[i])

	for i in range(0, len(matrix[0])):
		X[i].append(datetimes[i].hour * 60 + datetimes[i].minute)
		X[i].append(datetimes[i].weekday())

	test_X = X
	test_datetimes = datetimes

	startup = []
	rampdown = []
	year_month_day = ""
	Now = DT.datetime.now()
	if Now.hour < 8:
		year_month_day = str(Now)[:11] 
	else:
		year_month_day = str(Now + DT.timedelta(1))[:11]

	for pre in fan_estimators:
		switch_list = []
		fan_status = pre.predict(X)
		window_fan_status = []
		for i in range(0, len(datetimes)-1):
			if datetimes[i].hour >= 5 and datetimes[i].hour < 8:
				window_fan_status.append(fan_status[i])
				if (fan_status[i] == 0 and fan_status[i+1] == 1):
					startup.append(datetimes[i])
					#year_month_day = str(datetimes[i])[:11]

	#granularity in minutes
	decision_granularity = 5
	threshold_percentage = 0.2

	votes = {}
	fan_numbers = len(startup)
	for s in startup:
		minutes_offset = s.hour * 60 + s.minute
		first = (minutes_offset / decision_granularity) * decision_granularity 
		end = first + decision_granularity 

		recommendation = first

		if end - minutes_offset < minutes_offset - first:
			recommendation = end

		try:
			votes[recommendation] += 1
		except:
			votes[recommendation] = 1


	final_rec = DT.time(7, 0)

	first_set_seen = False
	fans_on_sum = 0
	for time in sorted(votes):
		fans_on_sum += votes[time]
		if not(first_set_seen) and fans_on_sum > threshold_percentage * fan_numbers:
			final_rec = DT.time(time/60, time%60)
			first_set_seen = True 

		print str(time/60) + ":" + str(time%60) + "\t" + str(votes[time])

	
	startup_rec = year_month_day + str(final_rec)

	[time, occupancy] = Occupancy_TimeSeries

	##
	# Default time for ramping down
	rampdown_rec = DT.datetime.now()
	while rampdown_rec.hour != 16:
		rampdown_rec += DT.timedelta(0, 1)

	refined_actuals = []
	[actual_startups, actual_rampdowns] = actuals
	for i in actual_rampdowns:
		if i.hour > 13 and i.hour < 18:
			print i
			refined_actuals.append(i)

	filtered_X = []
	filtered_Y = []
	pointer = 0
	train_indices = []
	for i in xrange(len(train_datetimes)):
		if pointer >= len(refined_actuals):
			break

		timestamp = train_datetimes[i]

		if refined_actuals[pointer].date() == timestamp.date() and timestamp.hour > 13 and timestamp.hour < 18:	
			filtered_X.append(timestamp)
			if timestamp < refined_actuals[pointer]:
				filtered_Y.append(0)
			else:
				filtered_Y.append(1)
			train_indices.append(i)

		elif refined_actuals[pointer].date() < timestamp.date():
			pointer += 1

		else:
			continue

	print "Building models for ramp-down..."

	time_of_day_cov = []
	weekday_cov = []
	for i in xrange(len(train_matrix[0])):
		time_of_day_cov.append(train_datetimes[i].hour * 60 + train_datetimes[i].minute)
		weekday_cov.append(train_datetimes[i].weekday())
		
	train_matrix.append(time_of_day_cov)
	train_matrix.append(weekday_cov)

	train_X = numpy.array(numpy.matrix(train_matrix).transpose())
	train_X = [train_X[i] for i in train_indices]

	if train_X != []:
		estimator = ExtraTreesClassifier()
		estimator.fit(train_X, filtered_Y)
		y = estimator.predict(test_X)

	for i in range(1, len(y)):
		if test_datetimes[i].hour > 14 and test_datetimes[i].hour < 18:
			if y[i] == 1 and y[i-1] == 0:
				rampdown_rec = test_datetimes[i]
				break

	return startup_rec, rampdown_rec

	print "Predictions were made."

def reconstruct():

	print "Reconstructing the covariate matrix"


def model():

	print "Building models..."


def commit():
	
	print "Commiting forecasts..."


def recommend(config_file, config_key, logger):

	logger.info("Building section name: %s" % config_key)
	Dataset, Occupancy_TimeSeries, actuals = covariate(config_file, config_key, 30)
	startup, rampdown = recommend_action(Dataset, Occupancy_TimeSeries, actuals, logger)

	print startup

	cparser = cfgparse.ConfigParser()

	cparser.add_option('results_db_server', dest='results_db_server', type='string', keys=config_key)
	cparser.add_option('results_db', dest='results_db', type='string', keys=config_key)
	cparser.add_option('results_db_user', dest='results_db_user', type='string', keys=config_key)
	cparser.add_option('results_db_pwd', dest='results_db_pwd', type='string', keys=config_key)

	cparser.add_option('results_table_startup', dest='results_table_startup', type='string', keys=config_key)
	cparser.add_option('results_table_rampdown', dest='results_table_rampdown', type='string', keys=config_key)

	cparser.add_file(config_file)
	options = cparser.parse()

	connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(options.results_db_server, options.results_db, options.results_db_user, options.results_db_pwd))
	cursor = connection.cursor()

	now = DT.datetime.now()
	startup_day = DT.datetime.strptime(startup, '%Y-%m-%d %H:%M:%S')

	query = "INSERT INTO [{0}] (Run_DateTime, Prediction_DateTime) VALUES ('{1}', '{2}')"
	query = query.format(options.results_table_startup, str(now)[:19], startup)

	if not(now.hour > 4 and now.hour < 13) and not(startup_day.weekday() == 5 or startup_day.weekday() == 6):
		logger.info("Commiting startup time %s" % str(startup))
		cursor.execute(query)
	else:
		logger.info("Time out of range for startup recommendation.")

	query = "INSERT INTO [{0}] (Run_DateTime, Prediction_DateTime) VALUES ('{1}', '{2}')"
	query = query.format(options.results_table_rampdown, str(now)[:19], str(rampdown)[:19])

	if not(now.hour > 14 and now.hour < 20) and not(rampdown.weekday() == 5 or rampdown.weekday() == 6):
		logger.info("Commiting rampdown time %s" % str(rampdown))
		cursor.execute(query)
	else:
		logger.info("Time out of range for rampdown recommendation.")

	cursor.commit()
	cursor.close()
	connection.close()


def main(argv):

	###
	# Boilerplate to set up cParser
	###
	version = "%prog 0.1"
	usage = "usage: %prog [options]"

	oparser = optparse.OptionParser(usage=usage, version=version,description=__doc__)
	cparser = cfgparse.ConfigParser()


	setup(oparser, cparser, _module)

	options, args = cparser.parse(oparser, argv)


	lgr = log_from_config(options, _module)
	lgr.info('*** %s' % _module)
	
	arg_count = len(args)

	run_ts = dt.datetime.now()
	lgr.info('run time: %s' % run_ts)

	###
	# Setting Up Config Parser 
	###

	cparser = cfgparse.ConfigParser()
	cparser.add_option('base_dir', dest='base_dir', type='string', keys='DEFAULT')
	cparser.add_option('building_ids', dest='building_ids', type='string', keys='DEFAULT')
	cparser.add_file('../config.ini')
	options = cparser.parse()

	if len(argv) == 1:
		buildings = options.building_ids.replace(' ', '').split(',')
		for building in buildings:
			recommend('../config.ini', building, lgr)

	elif len(argv) == 2:
		building = argv[1]
		recommend('../config.ini', building, lgr)

	else:
		print "Wrong usage!"
	
if __name__ == '__main__':
	main(sys.argv)

