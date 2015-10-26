#!/bin/env python

import subprocess
import sys
import os
import datetime
import math
import cfgparse
import tempfile
import math
import numpy
from sklearn.metrics import mean_squared_error

from collections import OrderedDict
import traceback

try:
	import cPickle as pickle
except ImportError:
	import pickle

from common_rudin.db_utils import connect
import common_rudin.common as common

BASE_TS = datetime.datetime(2009, 1, 1)

def ts_to_time_index(ts):
	""" compute number of seconds since the base date """
	return (ts - BASE_TS).total_seconds()


def time_index_to_ts(time_index):
		return self.BASE_TS + datetime.timedelta(seconds=time_index)


def filter_data(data_dict, forecast_start_ts, options, lgr):
	""" filter out data data from other seasons and/or irrelevant data
		the start and end markers (month, day, hour and minute combination) specify
		the boundaries for the data to keep
	"""
	radius_td = datetime.timedelta(days=options.training_radius)
	ONE_YEAR = datetime.timedelta(days=365)
	year_ago_lower_bound_ts = forecast_start_ts - ONE_YEAR - radius_td
	year_ago_upper_bound_ts = forecast_start_ts - ONE_YEAR + radius_td

	filtered_data = OrderedDict([])
	for ts, val in data_dict.iteritems():
		if ts <= forecast_start_ts and \
		  (ts >= forecast_start_ts - radius_td or \
		   (ts >= year_ago_lower_bound_ts and ts <= year_ago_upper_bound_ts)):

			# 
			if ts.minute % options.forecast_granularity != 0:
				continue

			# ignore seconds and microseconds
			ts -= datetime.timedelta(seconds=ts.second,
				microseconds=ts.microsecond)

			filtered_data[ts] = val
	
	#return [filtered_data, filtered_data.keys()]
	return [data_dict, filtered_data.keys()]



# def filter_data(data_dict, options, lgr):
	# """ filter data """

	# filtered_data = OrderedDict([])
	# for ts, value in data_dict.iteritems():

		# if ts.minute % self.options.forecast_granularity != 0:
			# continue

		##ignore seconds and microseconds
		# ts -= datetime.timedelta(seconds=ts.second,
			# microseconds=ts.microsecond)
		# filtered_data[ts] = value

	# return [filtered_data, filtered_data.keys()]



def interpolate_data(data_dict, options, lgr):
	""" interpolate data: selectively fill small gaps """

	interp_data = OrderedDict([])
	TWO_HOURS = datetime.timedelta(hours=2)
	gap_td  = datetime.timedelta(minutes=options.forecast_granularity)

	if gap_td >= TWO_HOURS:
		lgr.warning('data interpolation skipped. forecast granularity too large')
		return [data_dict, data_dict.keys()]

	prev_ts, prev_value = None, None
	for ts, value in data_dict.iteritems():

		if prev_ts:
			interp_keys = []
			if ts - prev_ts >= TWO_HOURS:

				# find timestamps to interpolate data for
				temp_ts = adjust_ts(prev_ts, options.forecast_granularity,
					options, lgr)

				# adjusted prev_ts may be just prev_ts with seconds and milli-
				# second fields cleared
				# if temp_ts < prev_ts:
					# temp_ts += gap_td

				while temp_ts < ts and temp_ts > prev_ts:
					interp_keys.append(temp_ts)
					temp_ts += gap_td

			if len(interp_keys):
				# interpolate
				interp_values = numpy.interp(
					map(ts_to_time_index, interp_keys),
					map(ts_to_time_index, [prev_ts, ts]), [prev_value, value],
					None, None)

				lgr.info('interpolation interval: (%s, %s)' % (prev_ts, ts))
				lgr.info('keys = %s\nvalues = %s' % (interp_keys, interp_values))

				# insert interpolated data into dict 
				for i, ts in enumerate(interp_keys):
					interp_data[ts] = interp_values[i]

		interp_data[ts] = value
		#interp_data_keys.append(ts)
		prev_ts, prev_value = ts, value

	return [interp_data, interp_data.keys()]



def interpolate_data2(data_dict, options, lgr):
	""" interpolate data: selectively fill small gaps """

	interp_data = OrderedDict([])
	TWO_HOURS = datetime.timedelta(hours=2)
	# we ignore small secind and milliseconf fields; so two readings
	# may actually be apart by upto 16 minutes and it should still be normal
	allowed_gap = datetime.timedelta(minutes=options.forecast_granularity + 1)
	gap_td  = datetime.timedelta(minutes=options.forecast_granularity)

	lgr.info('interpolating...')
	# if gap_td >= TWO_HOURS:
		# lgr.warning('data interpolation skipped. forecast granularity too large')
		# return [data_dict, data_dict.keys()]

	# find timestamps to interpolate data for
	prev_ts = None
	interp_keys = []
	for ts in data_dict.keys():

		if prev_ts:
			tmp_gap = ts - prev_ts

			#if tmp_gap > allowed_gap:
				#lgr.info('gap = %s; (%s, %s)' % (tmp_gap, prev_ts, ts))

			if tmp_gap > allowed_gap and tmp_gap <= TWO_HOURS:

				temp_ts = adjust_ts(prev_ts, options.forecast_granularity,
					options, lgr)

				#lgr.info('adjusted prev ts: %s' % temp_ts)
				# adjusted prev_ts may be just prev_ts with seconds and milli-
				# second fields cleared
				if temp_ts <= prev_ts:
					temp_ts += gap_td
				#lgr.info('adjusted prev ts 2: %s' % temp_ts)

				new_keys = []
				while temp_ts < ts and temp_ts > prev_ts:
					new_keys.append(temp_ts)
					interp_keys.append(temp_ts)
					temp_ts += gap_td
				#lgr.info('new keys: %s' % new_keys)

		prev_ts = ts

	# interpolate
	interp_values = None
	if len(interp_keys):
		#lgr.info('keys to interpolate: %s' % interp_keys)
		interp_values = numpy.interp(
			map(ts_to_time_index, interp_keys),
			map(ts_to_time_index, data_dict.keys()), data_dict.values(),
			None, None)

		# merge interpolated data and observed data 
		# lgr.info(len(interp_keys))
		# lgr.info(len(interp_values))
		tmp_dict = dict(data_dict.items() + zip(interp_keys, list(interp_values)))
		sorted_keys = sorted(tmp_dict.keys()) #, key=tmp_dict.__getitem__)
		for key in sorted_keys:
			interp_data[key] = tmp_dict[key]

	else:
		interp_data = data_dict
					
	return [interp_data, interp_data.keys()]



def validate_labels(labels):
	""" validate and cleanup labels
		- Negative values are set to zero
	"""
	new_labels = []
	for label in labels:
		if label < 0:
			new_labels.append(0.0)
		else:
			new_labels.append(label)
	return new_labels



def compute_deltas(data_dict, options, lgr):
	""" compute delta for successive data-points """

	prev_ts, prev_data = None, None
	deltas = OrderedDict([])
	gap_td = datetime.timedelta(minutes=options.forecast_granularity)

	for ts, data in data_dict.iteritems():
		if prev_ts and ts - prev_ts == gap_td:
			deltas[ts] = data - prev_data

		prev_ts, prev_data = ts, data

	return deltas



def create_temp_file(options, lgr, file_suffix='', close_fd=True):
	""" create temporary file; caller must delete the file after use """

	fd, f_name = tempfile.mkstemp(suffix=file_suffix,
		dir=options.temp_dir, text=True)
	if close_fd:
		os.close(fd)
		fd = None

	return [f_name, fd]



def add_weather_config_options(mod_cfggroup, module):
	"""
	add building configuration settings to be read from config file
	"""

	mod_cfggroup.add_option('weather_db', keys=module)
	mod_cfggroup.add_option('weather_db_server', keys=module)

	mod_cfggroup.add_option('weather_table', keys=module)
	mod_cfggroup.add_option('weather_forecast_table', keys=module)

	mod_cfggroup.add_option('weather_db_user', keys=module)
	mod_cfggroup.add_option('weather_db_pwd', keys=module)



def add_tenant_config_options(mod_cfggroup, tenant_id):
	"""
	add building configuration settings to be read from config file
	"""

	mod_cfggroup.add_option('tenant_db', keys=tenant_id)
	mod_cfggroup.add_option('tenant_db_server', keys=tenant_id)

	# mod_cfggroup.add_option('bms', keys=building_id)
	# mod_cfggroup.add_option('has_steam_supply', type='int', keys=building_id)

	mod_cfggroup.add_option('db_user', keys=tenant_id)
	mod_cfggroup.add_option('db_pwd', keys=tenant_id)
	
	mod_cfggroup.add_option('weather_station_id', keys=tenant_id)

	mod_cfggroup.add_option('tenant_floors', keys=tenant_id)
	# mod_cfggroup.add_option('floor_quadrants', keys=tenant_id)

	mod_cfggroup.add_option('results_db', keys=tenant_id)
	mod_cfggroup.add_option('results_db_server', keys=tenant_id)

	mod_cfggroup.add_option('results_db_user', keys=tenant_id)
	mod_cfggroup.add_option('results_db_pwd', keys=tenant_id)
	
	mod_cfggroup.add_option('holiday_table', keys=tenant_id)

	mod_cfggroup.add_option('building_open_hour', type='int', keys=tenant_id)
	mod_cfggroup.add_option('building_close_hour', type='int', keys=tenant_id)

	# electric
	mod_cfggroup.add_option('electric_data_file', keys=tenant_id)
	mod_cfggroup.add_option('electric_load_table', keys=tenant_id)
	mod_cfggroup.add_option('save_tenant_data', type='int', keys=tenant_id)
	mod_cfggroup.add_option('electric_load_table_total', keys=tenant_id)
	mod_cfggroup.add_option('results_table_electric', keys=tenant_id)
	mod_cfggroup.add_option('xval_results_table_electric', keys=tenant_id)
	mod_cfggroup.add_option('train_covariate_filename_fmt_electric',
		keys=tenant_id)
	mod_cfggroup.add_option('xval_results_table_electric', keys=tenant_id)
	mod_cfggroup.add_option('score_table_electric', keys=tenant_id)
	
	mod_cfggroup.add_option('save_results', type='int', keys=tenant_id)
	# alarms
	mod_cfggroup.add_option('alarms_table', keys=tenant_id)
	mod_cfggroup.add_option('sign_prog', keys=tenant_id)

	# add building id as an option
	mod_cfggroup.add_option('tenant_id', keys=tenant_id,
		default=tenant_id)
	


def add_bldg_config_options(mod_cfggroup, building_id):
	"""
	add building configuration settings to be read from config file
	"""

	mod_cfggroup.add_option('building_db', keys=building_id)
	mod_cfggroup.add_option('building_db_server', keys=building_id)

	mod_cfggroup.add_option('bms', keys=building_id)
	mod_cfggroup.add_option('has_steam_supply', type='int', keys=building_id)

	mod_cfggroup.add_option('db_user', keys=building_id)
	mod_cfggroup.add_option('db_pwd', keys=building_id)

	mod_cfggroup.add_option('building_floors', keys=building_id)
	mod_cfggroup.add_option('floor_quadrants', keys=building_id)
	mod_cfggroup.add_option('zones', keys=building_id)

	mod_cfggroup.add_option('weather_station_id', keys=building_id)

	mod_cfggroup.add_option('results_db', keys=building_id)
	mod_cfggroup.add_option('results_db_server', keys=building_id)
	# Added the next 2 AGB
	mod_cfggroup.add_option('results_db_user', keys=building_id)
	mod_cfggroup.add_option('results_db_pwd', keys=building_id)
	
	mod_cfggroup.add_option('holiday_table', keys=building_id)

	mod_cfggroup.add_option('results_table', keys=building_id)
	mod_cfggroup.add_option('prediction_derived_results_table', keys=building_id)
	mod_cfggroup.add_option('space_temp_deltas_table', keys=building_id)
	mod_cfggroup.add_option('space_temp_tablename_format', keys=building_id)

	mod_cfggroup.add_option('building_open_hour', type='int', keys=building_id)
	mod_cfggroup.add_option('building_close_hour', type='int', keys=building_id)

	mod_cfggroup.add_option('xval_results_table', keys=building_id)

	# for cross-validate module
	mod_cfggroup.add_option('train_covariate_filename_fmt', keys=building_id)

	# for scoring module
	mod_cfggroup.add_option('score_table', keys=building_id)

	# for steam predictions
	mod_cfggroup.add_option('steam_demand_table', keys=building_id)
	mod_cfggroup.add_option('results_table_steam', keys=building_id)
	mod_cfggroup.add_option('xval_results_table_steam', keys=building_id)
	# for steam cross-validation
	mod_cfggroup.add_option('train_covariate_filename_fmt_steam',
		keys=building_id)
	# for steam predictions scoring
	mod_cfggroup.add_option('score_table_steam', keys=building_id)
	mod_cfggroup.add_option('steam_data_file', keys=building_id)

	# electric
	mod_cfggroup.add_option('electric_data_file', keys=building_id)
	mod_cfggroup.add_option('electric_load_table', keys=building_id)
	mod_cfggroup.add_option('results_table_electric', keys=building_id)
	mod_cfggroup.add_option('xval_results_table_electric', keys=building_id)
	mod_cfggroup.add_option('train_covariate_filename_fmt_electric',
		keys=building_id)
	mod_cfggroup.add_option('xval_results_table_electric', keys=building_id)
	mod_cfggroup.add_option('score_table_electric', keys=building_id)

	mod_cfggroup.add_option('feed_type', keys=building_id)

	mod_cfggroup.add_option('occupancy_table', keys=building_id)
	mod_cfggroup.add_option('predict_occupancy', type='int', keys=building_id)
	mod_cfggroup.add_option('xval_results_table_occupancy', keys=building_id)
	mod_cfggroup.add_option('results_table_occupancy', keys=building_id)
	mod_cfggroup.add_option('score_table_occupancy', keys=building_id)
	mod_cfggroup.add_option('train_covariate_filename_fmt_occupancy', keys=building_id)
	
	mod_cfggroup.add_option('save_results', type='int', keys=building_id)
	# alarms
	mod_cfggroup.add_option('alarms_table', keys=building_id)
	mod_cfggroup.add_option('sign_prog_steam', keys=building_id)
	mod_cfggroup.add_option('sign_prog_occupancy', keys=building_id)
	mod_cfggroup.add_option('sign_prog_electric', keys=building_id)
	mod_cfggroup.add_option('sign_prog_space_temp', keys=building_id)
	
	mod_cfggroup.add_option('fan_table', keys=building_id)
	
	# ASC
	mod_cfggroup.add_option('thermal_asc_spc_temp_output_table',
		keys=building_id)
	mod_cfggroup.add_option('thermal_asc_electric_output_table',
		keys=building_id)
	mod_cfggroup.add_option('thermal_asc_steam_output_table',
		keys=building_id)
	mod_cfggroup.add_option('thermal_asc_occupancy_output_table',
		keys=building_id)
	mod_cfggroup.add_option('thermal_asc_spc_temp_score_table',
		keys=building_id)
	mod_cfggroup.add_option('thermal_asc_electric_score_table',
		keys=building_id)
	mod_cfggroup.add_option('thermal_asc_steam_score_table',
		keys=building_id)
	mod_cfggroup.add_option('thermal_asc_occupancy_score_table',
		keys=building_id)
	

	# scoring-related settings
	#mod_cfggroup.add_option('scoring_start_hour', type='int', keys=building_id)
	#mod_cfggroup.add_option('scoring_end_hour', type='int', keys=building_id)
	#mod_cfggroup.add_option('score_weekends', type='int', keys=building_id)

	# add building id as an option
	mod_cfggroup.add_option('building_id', keys=building_id,
		default=building_id)



def load_bldg_config(building_id, oparser, cparser, argv, options, lgr,
		reinistantiate_parser=True):
	""" load building and related weather configuration setting
		from config file
	"""

	# re-instantiate cparser; this is required because
	# cfgparse does not allow duplicate entries
	if reinistantiate_parser:
		cparser = cfgparse.ConfigParser()
		common.setup_cparser(cparser, building_id)

	# load building configuration
	bldg_cfggroup = cparser.add_option_group(building_id)
	add_bldg_config_options(bldg_cfggroup, building_id)

	lgr.info('loading configuration for building_id: %s' % building_id)
	options, _ = cparser.parse(oparser, argv)

	lgr.info('loading weather station configuration: %s' % 
		options.weather_station_id)

	# add weather; the config file must be re-read here to read the
	# correct weather station section
	weather_cfggroup = cparser.add_option_group(
		options.weather_station_id)
	add_weather_config_options(weather_cfggroup,
		options.weather_station_id)
	options, _ = cparser.parse(oparser, argv)

	return options



def load_tenant_config(tenant_id, oparser, cparser, argv, options, lgr,
		reinistantiate_parser=True):
	""" load building and related weather configuration setting
		from config file
	"""

	# re-instantiate cparser; this is required because
	# cfgparse does not allow duplicate entries
	if reinistantiate_parser:
		cparser = cfgparse.ConfigParser()
		common.setup_cparser(cparser, tenant_id)

	# load building configuration
	tenant_cfggroup = cparser.add_option_group(tenant_id)
	add_tenant_config_options(tenant_cfggroup, tenant_id)

	lgr.info('loading configuration for tenant_id: %s' % tenant_id)
	options, _ = cparser.parse(oparser, argv)

	lgr.info('loading weather station configuration: %s' % 
		options.weather_station_id)

	# add weather; the config file must be re-read here to read the
	# correct weather station section
	weather_cfggroup = cparser.add_option_group(
		options.weather_station_id)
	add_weather_config_options(weather_cfggroup,
		options.weather_station_id)
	options, _ = cparser.parse(oparser, argv)

	return options



def parse_value_list(value_list, type=str):
	""" parse comma separated list of values """

	value_list = value_list.strip()
	if not len(value_list):
		return []

	values = value_list.split(',')
	# remove surrounding spaces, if any
	values = map(str.strip, values)
	# convert to desired type
	return map(type, values)



def get_floors_quadrants(options, lgr):
	""" get building floor and quadrant information and validate it """

	bldg_floors = parse_value_list(options.building_floors)
	bldg_floor_quadrants = parse_value_list(options.floor_quadrants)
	sign_progs = parse_value_list(options.sign_prog_space_temp)
	zones = parse_value_list(options.zones)
	lgr.info('zones: >%s<' % zones)

	if (len(bldg_floors) != len(bldg_floor_quadrants)
	   or len(bldg_floors) != len(sign_progs)
	   or (len(zones) and len(bldg_floors) != len(zones))):
		lgr.info('building floor count, quadrant count & sign_prog count must match')
		lgr.info('zones, if specified, must be provided for all floor-quandrats')
		#sys.exit(1)
		raise Exception('configuration error')

	return [bldg_floors, bldg_floor_quadrants, sign_progs, zones]



def get_optimal_model_params_bldg(hour, forecast_start_ts, params_table,
		options, lgr):
	""" get cross-validation results from database for steam """

	# connect to the database
	cnxn, cursr = connect(options.db_driver, options.results_db_user, options.results_db_pwd,
		options.results_db, options.results_db_server)

	tab = '[%s].dbo.[%s]' % (options.results_db,
		params_table) #options.xval_results_table_steam)

	sub_qry = """
		(SELECT Run_DateTime, c, gamma, avg_error
		 FROM %s
		 WHERE
		   [Hour] = ?
		   AND Run_DateTime = (SELECT MAX(Run_DateTime) FROM %s
								WHERE [Hour] = ? AND Run_DateTime < ?)) t
	""" % (tab, tab)

	qry = """
		SELECT Run_DateTime, c, gamma
		FROM %s
		WHERE avg_error = (SELECT MIN(avg_error) FROM %s)
	""" % (sub_qry, sub_qry)

	#lgr.info(qry)
	cursr.execute(qry, hour, hour, forecast_start_ts,
		hour, hour, forecast_start_ts)

	newest_run_ts, opt_c, opt_gamma = None, None, None

	for row in cursr.fetchall():
		newest_run_ts, opt_c , opt_gamma = row
		break

	cnxn.close()

	if not newest_run_ts:
		lgr.critical('>>>>>>>cross-validation results not found. using defaults<<<<<<<<')
		return [100, 0.001]

	if datetime.datetime.now() - newest_run_ts > datetime.timedelta(days=1):
		lgr.warning('cross-validation results > 24h old (%s)' % newest_run_ts)
	return [opt_c, opt_gamma]



def get_optimal_model_params(hour, floor, quadrant, forecast_start_ts,
	options, lgr):
	""" get cross-validation results from database """

	# TODO: use forecast_start_ts
	# connect to the database
	cnxn, cursr = connect(options.db_driver, options.results_db_user,
		options.results_db_pwd, options.results_db, options.results_db_server)

	tab = '[%s].dbo.[%s]' % (options.results_db, options.xval_results_table)

	sub_qry = """
		(SELECT Run_DateTime, c, gamma, avg_error
		 FROM %s
		 WHERE Floor = ?
		   AND Quadrant = ?
		   AND [Hour] = ?
		   AND Run_DateTime = (SELECT MAX(Run_DateTime) FROM %s
								WHERE Floor = ?
								AND Quadrant = ?
								AND [Hour] = ?)) t
	""" % (tab, tab)

	qry = """
		SELECT Run_DateTime, c, gamma
		FROM %s
		WHERE avg_error = (SELECT MIN(avg_error) FROM %s)
	""" % (sub_qry, sub_qry)

	#lgr.info(qry)
	cursr.execute(qry, floor, quadrant, hour, floor, quadrant,
		hour, floor, quadrant, hour, floor, quadrant, hour)

	newest_run_ts, opt_c, opt_gamma = None, None, None

	for row in cursr.fetchall():
		newest_run_ts, opt_c , opt_gamma = row
		break

	cnxn.close()

	if not newest_run_ts:
		lgr.critical('>>>>>>>cross-validation results not found. using defaults<<<<<<<<')
		return [100, 0.001]
		#sys.exit(1)

	if datetime.datetime.now() - newest_run_ts > datetime.timedelta(days=1):
		lgr.warning('cross-validation results > 24h old (%s)' % newest_run_ts)
	return [opt_c, opt_gamma]



def compute_prediction_derivatives(forecast_start_ts, predictions,
		options, lgr):
	""" compute prediction-derived data """

	pred_drvtvs = []

	# n-hour vane slope
	gap_hours = 2 # TODO: move to config_master.json
	gap_td = datetime.timedelta(hours=gap_hours)
	target_ts = forecast_start_ts + gap_td

	slope = None
	if target_ts in predictions and forecast_start_ts in predictions:
		source_prediction = predictions[forecast_start_ts]
		target_prediction = predictions[target_ts]
		slope = (target_prediction - source_prediction)*1.0/gap_hours
	else:
		lgr.warning('not enough data to compute prediction-derivatives')

	pred_drvtvs.append(slope)

	return pred_drvtvs


def save_space_temp_prediction_derivatives(run_ts, forecast_start_ts,
		pred_drvtvs, bldg_floor, floor_quadrant, options, lgr):
	""" save prediction-derived data """

	insert_stmt = """
		INSERT INTO [%s] 
			(Run_DateTime, Prediction_DateTime, Floor, Quadrant,
			 Predicted_Slope)
		VALUES (?, ?, ?, ?, ?)
	""" % (options.prediction_derived_results_table)

	# connect to database
	cnxn, cursr = connect(options.db_driver,
			options.results_db_user, options.results_db_pwd,
			options.results_db, options.results_db_server)

	cursr.execute(insert_stmt, run_ts, forecast_start_ts, bldg_floor,
		floor_quadrant, pred_drvtvs[0])
	
	cnxn.commit()
	cnxn.close()
	

def save_prediction(run_ts, hour, floor, quadrant, zone, labels, keys, sigma,
		options, lgr):
	""" save predictions to database """

	# validate key and label count
	if len(labels) != len(keys):
		lgr.critical('key count and label count must match. prediction save failed')
		#sys.exit(1)
		return

	zone_info_avlbl = False
	if zone:
		zone_info_avlbl = True
		
	insert_stmt = """
		INSERT INTO [%s] 
			(Run_DateTime, Prediction_DateTime, Floor, Quadrant,
			 Prediction_Value, Lower_Bound_95, Upper_Bound_95, Lower_Bound_68,
			 Upper_Bound_68)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
	""" % (options.results_table)
	
	insert_stmt_with_zone = """
		INSERT INTO [%s] 
			(Run_DateTime, Prediction_DateTime, Floor, Quadrant,
			 Prediction_Value, Lower_Bound_95, Upper_Bound_95, Lower_Bound_68,
			 Upper_Bound_68, Zone)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	""" % (options.results_table)

	# connect to database
	cnxn, cursr = connect(options.db_driver,
			options.results_db_user, options.results_db_pwd,
			options.results_db, options.results_db_server)

	insert_seq = []
	insert_seq_with_zone = []

	# compute 95%, 68.2% confidence interval
	lower_bound_95, upper_bound_95, lower_bound_68_2, upper_bound_68_2 = None, None, None, None
	if sigma:
		lower_bound_95 = sigma*math.log(0.025)
		upper_bound_95 = -lower_bound_95
		lower_bound_68_2 = sigma*math.log(0.159)
		upper_bound_68_2 = -lower_bound_68_2

	for i, ts in enumerate(keys):

		y_predict = labels[i]

		lower_limit_95, lower_limit_68_2 = None, None
		if sigma:
			lower_limit_95 = y_predict + lower_bound_95
			if lower_limit_95 < 0:
				lower_limit_95 = 0.0
			lower_limit_68_2 = y_predict + lower_bound_68_2
			if lower_limit_68_2 < 0:
				lower_limit_68_2 = 0.0

		row = (run_ts, ts, floor, quadrant, y_predict, lower_limit_95,
			y_predict + upper_bound_95 if sigma else None, lower_limit_68_2,
			y_predict + upper_bound_68_2 if sigma else None)

		if zone_info_avlbl:
			insert_seq_with_zone.append(row + (zone,))
		else:
			insert_seq.append(row)

	try:
		if zone_info_avlbl:
			cursr.executemany(insert_stmt_with_zone, insert_seq_with_zone)
		else:
			cursr.executemany(insert_stmt, insert_seq)

	except Exception, e:
		lgr.critical('saving forecast to database failed: %s' % e)
		#sys.exit(1)
		raise

	cnxn.commit()
	cnxn.close()



def save_prediction_steam_electric(run_ts, hour, labels, keys, table,
		sigma, options, lgr):
	""" save predictions to database """

	# validate key and label count
	if len(labels) != len(keys):
		lgr.critical('key count and label count must match. prediction save failed')
		#sys.exit(1)
		raise Exception('save failed')
	
	# Normalized table names have to be escaped wiht [] AGB
	insert_stmt = """
		INSERT INTO [%s] 
			(Run_DateTime, Prediction_DateTime, Prediction_Value,
			 Lower_Bound_95, Upper_Bound_95, Lower_Bound_68,
			 Upper_Bound_68)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	""" % (table)

	# connect to database
	cnxn, cursr = connect(options.db_driver,
			options.results_db_user, options.results_db_pwd,
			options.results_db, options.results_db_server)

	insert_seq = []

	# compute 95%, 68.2% confidence interval
	lower_bound_95, upper_bound_95, lower_bound_68_2, upper_bound_68_2 = None, None, None, None
	if sigma:
		lower_bound_95 = sigma*math.log(0.025)
		upper_bound_95 = -lower_bound_95
		lower_bound_68_2 = sigma*math.log(0.159)
		upper_bound_68_2 = -lower_bound_68_2

	for i, ts in enumerate(keys):

		y_predict = labels[i]

		lower_limit_95, lower_limit_68_2 = None, None
		if sigma:
			lower_limit_95 = y_predict + lower_bound_95
			if lower_limit_95 < 0:
				lower_limit_95 = 0.0
			lower_limit_68_2 = y_predict + lower_bound_68_2
			if lower_limit_68_2 < 0:
				lower_limit_68_2 = 0.0

		row = (run_ts, ts, y_predict, lower_limit_95,
			y_predict + upper_bound_95 if sigma else None, lower_limit_68_2,
			y_predict + upper_bound_68_2 if sigma else None)

		insert_seq.append(row)

	try:
		cursr.executemany(insert_stmt, insert_seq)
	except Exception, e:
		lgr.critical('saving forecast to database failed: %s' % e)
		raise

	cnxn.commit()
	cnxn.close()



def write_dict_to_csv(dict, out_file, column_name_list):
	""" write dictionary to csv file """

	with open(out_file, 'w') as f_out:

		# write header
		if column_name_list and len(column_name_list) > 0:
			f_out.write(','.join(map(str, column_name_list)) + '\n')

		# write content
		for k, v in dict.iteritems():
			f_out.write('%s,' % k)

			if isinstance(v, list):
				f_out.write(','.join(map(str, v)))
			else:
				f_out.write(str(v))
			f_out.write('\n')




def adjust_ts(ts, granularity, options, lgr):
	""" adjust timestamp to closest following forecast time and clear
		second and millisecond fields
	"""
	org_ts = ts

	# perform ceiling on minute field on start_ts
	if ts.minute % granularity != 0:
		ts += datetime.timedelta(minutes=granularity - ts.minute % granularity)

	# ignore seconds and microseconds
	ts -= datetime.timedelta(seconds=ts.second,
		microseconds=ts.microsecond)

	# if org_ts > ts:
		# ts += datetime.timedelta(minutes=granularity)

	return ts



def create_child_proc(args, out_file=None):
	""" create a new child process """

	if out_file:
		#std_out_file_path = os.path.abspath(out_file)
		#print 'before: %s, out file: %s' % (out_file, std_out_file_path)
		subprocess.check_call(args, stdout=open(os.path.abspath(out_file), 'w+'))
	else:
		subprocess.check_call(args)



def check_obs_avlblty(dt, obs_obj, options, lgr):
	""" returns True if observations are available between 4am and 7pm
		on date dt, False otherwise
	"""

	start_tm, end_tm = datetime.time(4), datetime.time(19)
	start_key = datetime.datetime.combine(dt, start_tm) # start ts
	end_key   = datetime.datetime.combine(dt, end_tm) # end ts
	# gap between observations
	delta = datetime.timedelta(minutes=options.forecast_granularity)
	
	# expected number of observations, assuming no gaps
	expected_count = (19 - 4)*(60.0/options.forecast_granularity)
	# actual observations found counter
	obs_count = 0

	key = start_key
	while key <= end_key:
		if key in obs_obj.data:
			obs_count = obs_count + 1
		key = key + delta

	# if more than threshold % observations found, return True
	if obs_count/expected_count > 0.9:
		return True
	return False


def score_predictions(obs_data, prediction_data, options, lgr):
	""" compute RMSE score """

	actual_data = []
	predicted_data = []
	miss_count = 0
	# maximum misses allowed before we discard the score
	max_miss_count = 0.15*24*60/options.forecast_granularity
	for ts, pred_value in prediction_data.iteritems():
		if options.debug:
			lgr.info('%s, %s' % (ts, pred_value))
			lgr.info(len(obs_data.keys()))
		
		if ts not in obs_data:
			lgr.info('%s not found' % ts)
		
		try:
			actual_data += [obs_data[ts]]
			predicted_data += [pred_value]
		except KeyError:
			miss_count += 1

	rmse = None
	#lgr.info(len(actual_data))
	#lgr.info(predicted_data)
	#lgr.info('%d, %d' % (miss_count, max_miss_count))
	if miss_count <= max_miss_count and len(actual_data):
		rmse = math.sqrt(mean_squared_error(actual_data, predicted_data))
	else:
		lgr.info('miss count exceeds threshold: %d' % miss_count)
	return rmse


def unpickler(fname, obj, lgr, options):
	""" unpickle file """

	file_name_full = os.path.join(options.temp_dir, fname)

	if os.path.isfile(file_name_full):
		try:
			with open(file_name_full, "rb") as file:
				obj = pickle.load(file)
		except Exception, e:
			lgr.warning('unpickle failed for %s: %s' % (file_name_full,
				traceback.format_exc()))
	else:
		lgr.warning('unpickle file not found: %s' % file_name_full)

	return obj



def pickler(fname, obj, lgr, options):
	""" pickle file """

	file_name_full = os.path.join(options.temp_dir, fname)
	try:
		with open(file_name_full, "wb") as file:
			pickle.dump(obj, file)
	except Exception, e:
		lgr.warning('pickle failed for %s: %s' % (file_name_full,
			traceback.format_exc()))
