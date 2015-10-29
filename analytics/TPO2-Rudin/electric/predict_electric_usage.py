#!/bin/env python

""" predict electrci demand of the building based on
	past observations and other covariates
"""

__version__ = '$Id'
__author__ = 'agagneja@ccls.columbia.edu'
_module = 'predict_electric_usage'

import os
import sys
from sets import Set
from collections import OrderedDict, deque
import datetime
import math
import optparse
import cfgparse
import traceback

from common_rudin.common import log_from_config, setup, setup_cparser
from common_rudin.compile_covariates import Compile_Covariates
import common_rudin.utils as utils
from common_rudin.failover import Failover

from electric import Electric
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

	# get building ids
	building_ids = utils.parse_value_list(options.building_ids)
	#weather_station_ids = utils.parse_value_list(options.weather_station_ids)

	model_type = 'electric_demand'
	reinstantiate_cparser = False
	for bldg_idx, building_id in enumerate(building_ids):

		if bldg_idx != 0:
			reinstantiate_cparser = True
		options = utils.load_bldg_config(building_id, oparser, cparser, argv,
			options, lgr, reinstantiate_cparser)

		#lgr.info('building id: %s, options: %s' % (building_id, options))

		# read weather data; weather is assumed to be same for all floors of a building
		weather_obj = Weather(lgr, options, forecast_start_ts)

		# read inputs
		electric_obj = Electric(lgr, options, forecast_start_ts, building_id)
		
		# compute similar weather days
		weather_obj.compute_similar_weather_day_cache(electric_obj.data.keys(),
			model_type)
		
		# load holidays 
		holidays_obj = Holidays(options, lgr)

		models = []
		failure_count = 0
		failover = None

		for hour_idx in range(0, 24):

			try:

				# compile train covariates
				train_covr_obj = Compile_Covariates(None, None, options, lgr,
					hour_idx, electric_obj.keys, electric_obj, weather_obj,
					holidays_obj, model_type)
	
				# generate test covariates
				test_covr_obj = Compile_Covariates(None, None, options, lgr,
					hour_idx, None, electric_obj, weather_obj, holidays_obj,
					model_type, False, forecast_start_ts,
					options.forecast_length, train_covr_obj.scaled_params_file)

				# fetch cross-validation results
				opt_c, opt_gamma = utils.get_optimal_model_params_bldg(hour_idx,
					forecast_start_ts, options.xval_results_table_electric,
					options, lgr)
				lgr.info('optimal C: %g, optimal gamma: %g' % (opt_c, opt_gamma))

				# _build model
				model_obj = Build_Model(train_covr_obj.covariates_file, opt_c,
					opt_gamma, options, lgr)

				# apply model
				p_labels = model_obj.apply_model(test_covr_obj.covariates_file)

				utils.save_prediction_steam_electric(run_ts, hour_idx, p_labels,
					test_covr_obj.actual_keys, options.results_table_electric,
					model_obj.model.get_svr_probability(), options, lgr)

			except Exception, e:

				lgr.info('Prediction failure for hour %d: %s' % (hour_idx,
					traceback.format_exc()))
			
				failure_count += 1

				try:
					# compute failover forecast
					failover = Failover(hour_idx, forecast_start_ts, run_ts,
						model_type, options.sign_prog_electric, options, lgr)
					p_labels_f = failover.compute_failover_forecast(electric_obj,
						weather_obj, holidays_obj)

					# save failover forecast
					utils.save_prediction_steam_electric(run_ts, hour_idx,
						p_labels_f, failover.keys, options.results_table_electric,
						None, options, lgr)
				except Exception, e:
					lgr.critical('Failover mechanism failed: %s' % (
						traceback.format_exc()))


		# indicate failure
		if options.save_results:
			try:

				if failure_count:
					failover.set_tpo_alarm(failure_count, model_type)
				else: # if TPO failure flag is already set, clear it if we have recovered
					failover = Failover(None, forecast_start_ts, run_ts,
						model_type, options.sign_prog_electric, options, lgr)
					failover.reset_tpo_alarm(model_type)
			
			except Exception, e:
				lgr.critical('Alarm set/reset failed: %s' % (
					traceback.format_exc()))



if __name__ == '__main__':
	main(sys.argv)