#!/bin/env python

""" predict space temperature in a given quadrant of a given floor based on
	past observed load and other covariates
"""

__version__ = '$Id'
__author__ = 'agagneja@ccls.columbia.edu'
_module = 'predict_space_temp'

import os
import sys
import traceback
from sets import Set
from collections import OrderedDict, deque
import datetime
import math
import optparse
import cfgparse

from common_rudin.common import log_from_config, setup, setup_cparser
from common_rudin.compile_covariates import Compile_Covariates
import common_rudin.utils as utils
from common_rudin.failover import Failover

from space_temp import Space_Temp
from space_temp_schneider import Space_Temp_Schneider
from common_rudin.weather import Weather
from common_rudin.build_model import Build_Model
from common_rudin.holidays import Holidays


def main(argv):
	""" driver function """

	if argv is None:
		argv = sys.argv

	version = "%prog 0.1"
	usage = "usage: %prog [options]"

	oparser = optparse.OptionParser(usage=usage, version=version,
		description=__doc__)
	cparser = cfgparse.ConfigParser()
	setup(oparser, cparser, _module)
	
	#mod_optgroup = oparser.add_option_group(_module)
	#mod_cfggroup = cparser.add_option_group(_module)
	#add_config_options(mod_optgroup, mod_cfggroup)

	options, args = cparser.parse(oparser, argv)

	lgr = log_from_config(options, _module)
	lgr.info('*** %s starting up' % _module)

	arg_count = len(args)

	run_ts = datetime.datetime.now()
	lgr.info('run time: %s' % run_ts)

	# determine forecast start time
	forecast_start_ts = None
	if arg_count == 1:
		forecast_start_ts = run_ts
	elif arg_count == 6:
		int_args = map(int, args[1:])
		forecast_start_ts = datetime.datetime(int_args[0], int_args[1], int_args[2],
			int_args[3], int_args[4])
	else:
		lgr.critical(args)
		oparser.error("incorrect number of arguments")

	forecast_start_ts = utils.adjust_ts(forecast_start_ts,
			options.forecast_granularity, options, lgr)
	lgr.info('forecast start time: %s' % forecast_start_ts)

	try:
		import multiprocessing
		lgr.info('cpu count: %d' % multiprocessing.cpu_count())
	except (ImportError,NotImplementedError):
		pass

	# get building ids
	building_ids = utils.parse_value_list(options.building_ids)
	#weather_station_ids = utils.parse_value_list(options.weather_station_ids)

	model_type = 'space_temp'
	reinstantiate_cparser = False
	for bldg_idx, building_id in enumerate(building_ids):

		if bldg_idx != 0:
			reinstantiate_cparser = True
		options = utils.load_bldg_config(building_id, oparser, cparser, argv,
			options, lgr, reinstantiate_cparser)

		#lgr.info('building id: %s, options: %s' % (building_id, options))

		bldg_floors, floor_quadrants, sign_progs, zones = utils.get_floors_quadrants(
														options, lgr)
		zone_info_avlbl = False
		if len(zones):
			zone_info_avlbl = True

		# read weather data; weather is assumed to be same for all floors of a building
		weather_obj = Weather(lgr, options, forecast_start_ts)
		
		# load holidays 
		holidays_obj = Holidays(options, lgr)

		zone = None
		# _build a model for each quadrant, floor pair
		for floor_idx, bldg_floor in enumerate(bldg_floors):

			floor_quadrant = floor_quadrants[floor_idx]
			# zone information is optional to maintain backward compatibility
			if zone_info_avlbl:
				zone = zones[floor_idx]
			sign_prog = sign_progs[floor_idx]

			lgr.info('processing floor %s, quadrant %s' % (bldg_floor,
				floor_quadrant))

			try:

				# read space temperature
				if options.feed_type == 'TPOSIF':
					space_temp_obj = Space_Temp(building_id, bldg_floor,
						floor_quadrant, lgr, options, forecast_start_ts)
				else:
					if options.bms != 'Schneider':
						space_temp_obj = Space_Temp(building_id, bldg_floor,
							floor_quadrant, lgr, options, forecast_start_ts)
					else:
						space_temp_obj = Space_Temp_Schneider(building_id,
							bldg_floor, floor_quadrant, lgr, options,
							forecast_start_ts)
						#continue

				# compute similar weather days
				weather_obj.compute_similar_weather_day_cache(
					space_temp_obj.data.keys(), model_type)

				predictions = {}
				failure_count = 0
				failover = None

				for hour_idx in range(0, 24):

					try:

						# compile train covariates
						train_covr_obj = Compile_Covariates(bldg_floor,
							floor_quadrant, options, lgr, hour_idx,
							space_temp_obj.keys, space_temp_obj, weather_obj,
							holidays_obj, model_type)

						# generate test covariates
						test_covr_obj = Compile_Covariates(bldg_floor,
							floor_quadrant, options, lgr, hour_idx, None,
							space_temp_obj, weather_obj, holidays_obj,
							model_type, False, forecast_start_ts,
							options.forecast_length,
							train_covr_obj.scaled_params_file)

						# fetch cross-validation results
						opt_c, opt_gamma = utils.get_optimal_model_params(
							hour_idx, bldg_floor, floor_quadrant,
							forecast_start_ts, options, lgr)
						lgr.info('optimal C: %g, optimal gamma: %g' % (
							opt_c, opt_gamma))

						# _build model
						model_obj = Build_Model(train_covr_obj.covariates_file, opt_c,
							opt_gamma, options, lgr)

						# apply model
						p_labels = model_obj.apply_model(test_covr_obj.covariates_file)

						p_labels = utils.validate_labels(p_labels)

						# save hourly predictions to global dict
						predictions.update(dict(zip(test_covr_obj.actual_keys, p_labels)))

						# save results
						if options.feed_type == 'TPOSIF':
							utils.save_prediction(run_ts, hour_idx, bldg_floor,
								floor_quadrant, zone, p_labels,
								test_covr_obj.actual_keys,
								model_obj.model.get_svr_probability(), options,
								lgr)
						else:
							if options.bms != 'Schneider':
								utils.save_prediction(run_ts, hour_idx,
									bldg_floor, floor_quadrant, zone, p_labels,
									test_covr_obj.actual_keys,
									model_obj.model.get_svr_probability(), options, lgr)
							else:
								space_temp_obj.save_predictions(run_ts, hour_idx,
									p_labels, test_covr_obj.actual_keys,
									model_obj.model.get_svr_probability())

					except Exception, e:

						lgr.info('Prediction failure for hour %d: %s' % (
							hour_idx, traceback.format_exc()))
						
						failure_count += 1
						
						try:

							# compute failover forecast
							failover = Failover(hour_idx, forecast_start_ts,
								run_ts, model_type, sign_prog, options, lgr)
							p_labels_f = failover.compute_failover_forecast(
								space_temp_obj, weather_obj, holidays_obj)

							# save failover predictions
							if options.feed_type == 'TPOSIF' or options.bms != 'Schneider':
								utils.save_prediction(run_ts, hour_idx, bldg_floor,
									floor_quadrant, zone, p_labels_f, failover.keys,
									None, options, lgr)
							else:
								space_temp_obj.save_predictions(run_ts, hour_idx,
									p_labels_f, failover.keys, None)

						except Exception, e:
							lgr.critical('Failover mechanism failed: %s' % (
								traceback.format_exc()))

				# indicate failure
				if options.save_results:
					try:

						if failure_count:
							failover.set_tpo_alarm(failure_count, model_type,
								bldg_floor, floor_quadrant)
						else: # if TPO failure flag is already set, clear it if we have recovered
							failover = Failover(None, forecast_start_ts,
								run_ts, model_type, sign_prog, options, lgr)
							failover.reset_tpo_alarm(model_type, bldg_floor, floor_quadrant)
	
					except Exception, e:
							lgr.critical('Alarm set/reset failed: %s' % (
								traceback.format_exc()))

				# compute prediction-derived data
				# pred_drvtvs = utils.compute_prediction_derivatives(
					# forecast_start_ts, predictions, options, lgr)
				#lgr.info(pred_drvtvs)
				# utils.save_space_temp_prediction_derivatives(run_ts,
					# forecast_start_ts, pred_drvtvs, bldg_floor,
					# floor_quadrant, options, lgr)

			except Exception, e:
				lgr.critical('An error occurred while generating model: %s' %
					traceback.format_exc())


if __name__ == '__main__':
	main(sys.argv)