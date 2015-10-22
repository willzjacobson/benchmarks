#!/bin/env python

__version__ = '$Id'
__author__ = 'ag2818@columbia.edu'
_module = 'thermal_asc_score_steam'

__doc__ = """ score steam thermal ASC predictions using observed data
		  """

import sys
from collections import OrderedDict
import math
import datetime

import optparse
import cfgparse
import traceback

from sets import Set

from common_rudin.db_utils import connect
from common_rudin.common import log_from_config, setup
import common_rudin.utils as utils

from steam.steam import Steam


def get_observed_data(building_id, options, lgr):
	""" """

	now_ts = datetime.datetime.now()

	# read space temperature data
	steam_obj = None
	if options.feed_type == 'TPOSIF':
		steam_obj = Steam(lgr, options, now_ts)
	else:
		lgr.critical('feed_type %s is no longer supported' %
			options.feed_type)

	keys = steam_obj.data.keys()
	lgr.info('%s, %s' % (keys[0], keys[-1]))
	return steam_obj


def get_prediction_data(dt, cnxn, options, lgr):
	""" read prediction data """

	# compute boundaries for prediction data
	start_ts = datetime.datetime.combine(dt, datetime.time.min)
	end_ts = datetime.datetime.combine(dt, datetime.time(23, 59, 59))
 
	select_qry = """
		SELECT t1.TIMESTAMP, SUM(t1.Value) 
		FROM [%s].[dbo].[%s] t1,
			(SELECT  MAX(RUNTIME) RUNTIME, TIMESTAMP, EQUIPMENT_NO
			 FROM [%s].[dbo].[%s]
			 WHERE RUNTIME < TIMESTAMP
			 GROUP BY TIMESTAMP, EQUIPMENT_NO) t2
		WHERE
			t1.TIMESTAMP > '%s' AND t1.TIMESTAMP < '%s'
			AND t1.RUNTIME      = t2.RUNTIME
			AND t1.TIMESTAMP    = t2.TIMESTAMP
			AND t1.EQUIPMENt_NO = t2.EQUIPMENT_NO
		GROUP BY t1.TIMESTAMP
		ORDER BY t1.TIMESTAMP
	""" % (options.results_db, options.thermal_asc_steam_output_table,
		options.results_db, options.thermal_asc_steam_output_table,
		start_ts, end_ts)

	cursr = cnxn.cursor()
	lgr.info(select_qry)
	cursr.execute(select_qry)

	prediction_data = OrderedDict([])
	for row in cursr.fetchall():
		pred_ts, prediction = row
		prediction_data[pred_ts] = prediction

	return prediction_data

	
def save_scores(score, as_of_dt, cnxn, options, lgr):
	""" save scores to db """

	if not score:
		return

	insert_stmt = """
		INSERT INTO [%s].dbo.[%s]
		(Date, RMSE)
		VALUES (?, ?)
	""" % (options.results_db, options.thermal_asc_steam_score_table)
	
	del_stmt = """DELETE FROM [%s].dbo.[%s]
		WHERE Date = '%s'""" % (options.results_db,
			options.thermal_asc_steam_score_table, as_of_dt)

	cursr = cnxn.cursor()

	insert_seq = []
	if options.debug:
		lgr.info(del_stmt)
	cursr.execute(del_stmt)
	cursr.execute(insert_stmt, as_of_dt, score)
	cnxn.commit()


def main(argv):
	""" driver function """

	if argv is None:
		argv = sys.argv

	version = '%prog 0.1'
	usage = 'usage: %prog [options]'

	oparser = optparse.OptionParser(usage=usage, version=version,
		description=__doc__)
	cparser = cfgparse.ConfigParser()
	setup(oparser, cparser, _module)

	options, args = cparser.parse(oparser, argv)
	arg_count = len(args)

	lgr = log_from_config(options, _module)
	lgr.info('*** %s starting up' % _module)
	
	run_ts = datetime.datetime.now()
	lgr.info('run time: %s, %d' % (run_ts, arg_count))

	# if no argument, compute results for previous day
	as_of_dt = None
	if arg_count == 1:
		as_of_dt = run_ts.date() - datetime.timedelta(days=1)

	# if a date is specified, 
	elif arg_count == 4:
		int_args = map(int, args[1:])
		as_of_dt = datetime.datetime(int_args[0], int_args[1], int_args[2])
	else:
		lgr.critical(args)
		oparser.error("incorrect number of arguments")

	# get building ids
	building_ids = utils.parse_value_list(options.building_ids)

	scores = []
	reinstantiate_cparser = False
	for bldg_idx, building_id in enumerate(building_ids):

		try:

			if bldg_idx != 0:
				reinstantiate_cparser = True
			options = utils.load_bldg_config(building_id, oparser, cparser, argv,
				options, lgr, reinstantiate_cparser)

			# check if building has steam supply
			if not options.has_steam_supply:
				lgr.info("building %s doen't have steam suply" % building_id)
				continue

			# fetch observed data
			observed_data_obj = get_observed_data(building_id, options, lgr)

			# connect to the database
			cnxn, cursr = connect(options.db_driver, options.results_db_user,
				options.results_db_pwd, options.results_db,
				options.results_db_server)

			# fetch predictions
			prediction_data = None
			if options.feed_type == 'TPOSIF':
				prediction_data = get_prediction_data(as_of_dt, cnxn,
					options, lgr)
			else:
				lgr.critical('feed_type %s is no longer supported' %
					options.feed_type)

			#if options.debug:
			lgr.info(prediction_data)

			# compute scores
			score = utils.score_predictions(observed_data_obj.data,
				prediction_data, options, lgr)
			lgr.info(score)

			lgr.info('saving scores')
			save_scores(score, as_of_dt, cnxn, options, lgr)

			# close connections
			cursr.close()
			cnxn.close()

		except Exception, e:
			lgr.critical('scoring %s failed: %s' % (building_id,
				traceback.format_exc()))

if __name__ == '__main__':
	main(sys.argv)