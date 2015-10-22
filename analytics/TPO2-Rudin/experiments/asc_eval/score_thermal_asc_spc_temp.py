#!/bin/env python

__version__ = '$Id'
__author__ = 'ag2818@columbia.edu'
_module = 'thermal_asc_score_spc_temp'

__doc__ = """ score space temperature, steam, occupancy and electric
				thermal ASC predictions using observed data
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

from space_temp.space_temp import Space_Temp

def get_observed_data(building_id, floor, quadrant, options, lgr):
	""" """

	now_ts = datetime.datetime.now()

	# read space temperature data
	space_temp_obj = None
	if options.feed_type == 'TPOSIF':
		space_temp_obj = Space_Temp(building_id, floor,
			quadrant, lgr, options, now_ts)
	else:
		lgr.critical('feed_type %s is no longer supported' %
			options.feed_type)

	keys = space_temp_obj.data.keys()
	lgr.info('%s, %s' % (keys[0], keys[-1]))
	return space_temp_obj


def get_prediction_data(floor, quadrant, dt, cnxn, options, lgr):
	""" read prediction data """

	# compute boundaries for prediction data
	start_ts = datetime.datetime.combine(dt, datetime.time.min)
	end_ts = datetime.datetime.combine(dt, datetime.time(23, 59, 59))

	select_qry = """
		SELECT t1.TIMESTAMP, t1.Value
		FROM [%s].[dbo].[%s] t1,
			(SELECT  MAX(RUNTIME) RUNTIME, TIMESTAMP
			 FROM [%s].[dbo].[%s]
			 WHERE Floor = '%s' AND Quadrant = '%s'
				AND EQUIPMENT_NO = '001'
				AND RUNTIME < TIMESTAMP
			 GROUP BY TIMESTAMP) t2
		WHERE
			t1.TIMESTAMP > '%s' AND t1.TIMESTAMP < '%s'
			AND EQUIPMENT_NO = '001'
			AND t1.Floor = '%s' AND t1.Quadrant = '%s'
			AND t1.RUNTIME = t2.RUNTIME
			AND t1.TIMESTAMP = t2.TIMESTAMP
		ORDER BY t1.TIMESTAMP
	""" % (options.results_db, options.thermal_asc_spc_temp_output_table,
		options.results_db, options.thermal_asc_spc_temp_output_table, floor,
		quadrant, start_ts, end_ts, floor, quadrant)

	cursr = cnxn.cursor()
	lgr.info(select_qry)
	cursr.execute(select_qry)

	prediction_data = OrderedDict([])
	for row in cursr.fetchall():
		pred_ts, prediction = row
		prediction_data[pred_ts] = prediction

	return prediction_data

	
def save_scores(scores, as_of_dt, cnxn, options, lgr):
	""" save scores to db """
	insert_stmt = """
		INSERT INTO [%s].dbo.[%s]
		(Date, Floor, Quadrant, RMSE)
		VALUES (?, ?, ?, ?)
	""" % (options.results_db, options.thermal_asc_spc_temp_score_table)
	
	del_stmt = """DELETE FROM [%s].dbo.[%s]
		WHERE Floor = ? AND Quadrant = ? AND
		Date = '%s'""" % (options.results_db,
			options.thermal_asc_spc_temp_score_table,
			as_of_dt)

	cursr = cnxn.cursor()

	insert_seq = []
	lgr.info(del_stmt)
	for flr, quad, rmse in scores:
		insert_seq.append((as_of_dt, flr, quad, rmse))
		cursr.execute(del_stmt, flr, quad)

	if len(insert_seq):
		cursr.executemany(insert_stmt, insert_seq)
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

			bldg_floors, floor_quadrants, _, _ = utils.get_floors_quadrants(
				options, lgr)

			# cross-validate for each (quadrant, floor) pair
			for floor_idx, bldg_floor in enumerate(bldg_floors):

				floor_quadrant = floor_quadrants[floor_idx]
				lgr.info('processing floor %s, quadrant %s' % (bldg_floor,
					floor_quadrant))

				# connect to the database
				cnxn, cursr = connect(options.db_driver, options.results_db_user,
					options.results_db_pwd, options.results_db,
					options.results_db_server)

				# fetch observed data
				observed_data_obj = get_observed_data(building_id, bldg_floor,
					floor_quadrant, options, lgr)

				# fetch predictions
				prediction_data = None
				if options.feed_type == 'TPOSIF':
					prediction_data = get_prediction_data(bldg_floor,
						floor_quadrant, as_of_dt, cnxn, options, lgr)
				else:
					lgr.critical('feed_type %s is no longer supported' %
						options.feed_type)

				lgr.info(prediction_data)

				# compute scores
				score = utils.score_predictions(observed_data_obj.data,
					prediction_data, options, lgr)
				lgr.info(score)
				scores.append((bldg_floor, floor_quadrant, score))

			lgr.info(scores)
			lgr.info('saving scores')
			save_scores(scores, as_of_dt, cnxn, options, lgr)

			# close connections
			cursr.close()
			cnxn.close()

		except Exception, e:
			lgr.critical('scoring %s failed: %s' % (building_id,
				traceback.format_exc()))

if __name__ == '__main__':
	main(sys.argv)