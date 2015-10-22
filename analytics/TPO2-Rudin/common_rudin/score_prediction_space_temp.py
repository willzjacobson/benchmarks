#!/bin/env python

__version__ = '$Id'
__author__ = 'agagneja@ccls.columbia.edu'
_module = 'score_prediction'

__doc__ = """ score space temperature, steam and electric predictions
				using observed data
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
from space_temp.space_temp_schneider import Space_Temp_Schneider


def get_observed_data(building_id, floor, quadrant, options, lgr):
	""" """

	now_ts = datetime.datetime.now()
	# read space temperature data
	# space_temp_obj = Space_Temp(building_id, floor, quadrant, lgr,
		# options, dummy_ts)
	if options.feed_type == 'TPOSIF':
		space_temp_obj = Space_Temp(building_id, floor,
			quadrant, lgr, options, now_ts)
	else:
		if options.bms != 'Schneider':
			space_temp_obj = Space_Temp(building_id, floor,
				quadrant, lgr, options, now_ts)
		else:
			space_temp_obj = Space_Temp_Schneider(building_id, floor,
				quadrant, lgr, options, now_ts)

	return space_temp_obj


MAE = 'MAE'
MSE = 'MSE'
MAPE = 'MAPE'

def score_predictions(observed_data, prediction_data, options, lgr):
	""" score predictions """

	# score predictions
	scores = {}
	missing_actual_vals = {}

	# DEBUG
	missing_obs_ts_dbg = []

	for pred_ts, prediction in prediction_data.iteritems():
		pred_dt = pred_ts.date()

		# check for and keep count of missing observations
		if pred_ts not in observed_data:
			if pred_dt in missing_actual_vals:
				missing_actual_vals[pred_dt] += 1
			else:
				missing_actual_vals[pred_dt] = 1

		else:
			observation = observed_data[pred_ts]

			# update scores
			mae = math.fabs(observation - prediction)
			mse = mae*mae
			# mape is not define when obervation is zero
			mape = None
			if observation:
				mape = math.fabs((observation - prediction)/observation)

			if pred_dt in scores:
				scores[pred_dt][MAE].append(mae)
				scores[pred_dt][MSE].append(mse)
				
				#scores[pred_dt][MAPE].append(mape)
				# mape can be None id observed data is 0
				if mape:
					scores[pred_dt][MAPE].append(mape)
			else:
				scores[pred_dt] = {MAE:[mae], MSE:[mse], MAPE:[mape]}

	# if we are missing more than 5% of the readings for any day, 
	# do not report error scores for that day
	dt_del_list = []
	for pred_dt, score in scores.iteritems():
		if MAE not in score \
		   or len(score[MAE]) < 0.95*24*60/options.forecast_granularity:
			lgr.info('>5%% observations missing for %s. Ignored. %d' % (
				pred_dt, len(score[MAE])))
			dt_del_list.append(pred_dt)

	# delete dates with missing data
	for pred_dt in dt_del_list:
		del scores[pred_dt]

	return scores


def save_scores(scores, cnxn, cursr, floor, quadrant, options, lgr):
	""" save scores """

	insert_stmt = """
		INSERT INTO [%s].dbo.[%s]
		(Prediction_Date, Floor, Quadrant, RMSE, MAE, MAPE)
		VALUES (?, ?, ?, ?, ?, ?)
	""" % (options.results_db, options.score_table)

	insert_seq = []
	for pred_dt, score in scores.iteritems():
		mse_list = score[MSE]
		mae_list = score[MAE]
		mape_list = score[MAPE]

		rmse, mae, mape = None, None, None
		if len(mse_list):
			rmse = math.sqrt(sum(mse_list)/len(mse_list))
		if len(mae_list):
			mae = sum(mae_list)/len(mae_list)
		if len(mape_list):
			mape = 100* (sum(mape_list)/len(mape_list))

		insert_seq.append((datetime.datetime.combine(pred_dt,
			datetime.time(0)), floor, quadrant, rmse, mae, mape))

	if len(insert_seq):
		cursr.execute("""DELETE FROM [%s].dbo.[%s]
			WHERE Floor = '%s' AND Quadrant = '%s'""" % (options.results_db,
			options.score_table, floor, quadrant))
		cursr.executemany(insert_stmt, insert_seq)
		cnxn.commit()



def get_prediction_data(cursr, floor, quadrant, options, lgr):
	""" retrieve prediction data """

	select_qry = """
		SELECT t1.Prediction_DateTime, t1.Prediction_Value
		FROM [%s].[dbo].[%s] t1,
			(SELECT  MAX(Run_DateTime) Run_DateTime, Prediction_DateTime
			 FROM [%s].[dbo].[%s]
			 WHERE Floor = '%s' AND Quadrant = '%s'
			 GROUP BY Prediction_DateTime) t2
		WHERE t1.Floor = '%s' AND t1.Quadrant = '%s'
			AND t1.Run_DateTime = t2.Run_DateTime
			AND t1.Prediction_DateTime = t2.Prediction_DateTime
		ORDER BY t1.Prediction_DateTime
	""" % (options.results_db, options.results_table, options.results_db,
		options.results_table, floor, quadrant, floor, quadrant)

	cursr.execute(select_qry)

	prediction_data = OrderedDict([])
	for row in cursr.fetchall():
		pred_ts, prediction = row
		# save predictions
		prediction_data[pred_ts] = prediction

	return prediction_data


def get_prediction_data_Schneider(cursr, floor, quadrant, options, lgr):
	""" retrieve prediction data Schneider """

	select_qry = """
		SELECT t1.Prediction_DateTime, t1.Prediction_Value
		FROM [%s].[dbo].[%s] t1,
			(SELECT  MAX(Run_DateTime) Run_DateTime, Prediction_DateTime
			 FROM [%s].[dbo].[%s]
			 WHERE Controller = '%s' AND SubController = '%s'
			 GROUP BY Prediction_DateTime) t2
		WHERE t1.Controller = '%s' AND t1.SubController = '%s'
			AND t1.Run_DateTime = t2.Run_DateTime
			AND t1.Prediction_DateTime = t2.Prediction_DateTime
		ORDER BY t1.Prediction_DateTime
	""" % (options.results_db, options.results_table, options.results_db,
		options.results_table, floor, quadrant, floor, quadrant)

	cursr.execute(select_qry)

	prediction_data = OrderedDict([])
	for row in cursr.fetchall():
		pred_ts, prediction = row
		# save predictions
		prediction_data[pred_ts] = prediction

	return prediction_data


def save_deltas(prediction_deltas, observed_deltas, floor, quadrant,
		cursr, cnxn, options, lgr):
	""" save prediction and observed data deltas to database """

	# create a master list of timestamps
	master_ts_set = Set(prediction_deltas.keys())
	master_ts_set.update(observed_deltas.keys())
	master_ts_list = sorted(list(master_ts_set))

	insert_seq = []
	for ts in master_ts_list:
		row = [None, None]

		if ts in prediction_deltas:
			row[0] = prediction_deltas[ts]
		if ts in observed_deltas:
			row[1] = observed_deltas[ts]

		#lgr.info('ts = %s: %s' % (ts, row))
		insert_seq.append((ts, floor, quadrant)+ tuple(row))

	table = '[%s].dbo.[%s]' % (options.results_db,
		options.space_temp_deltas_table)
	insert_stmt = """INSERT INTO %s
		(Timestamp, Floor, Quadrant, Predicted_Delta, Actual_Delta)
		VALUES (?, ?, ?, ?, ?)""" % table

	cursr.execute('DELETE FROM %s' % table)
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

	lgr = log_from_config(options, _module)
	lgr.info('*** %s starting up' % _module)

	# get building ids
	building_ids = utils.parse_value_list(options.building_ids)

	reinstantiate_cparser = False
	for bldg_idx, building_id in enumerate(building_ids):

		try:

			if bldg_idx != 0:
				reinstantiate_cparser = True
			options = utils.load_bldg_config(building_id, oparser, cparser, argv,
				options, lgr, reinstantiate_cparser)

			bldg_floors, floor_quadrants, _, _ = utils.get_floors_quadrants(options, lgr)

			# cross-validate for each (quadrant, floor) pair
			for floor_idx, bldg_floor in enumerate(bldg_floors):

				floor_quadrant = floor_quadrants[floor_idx]
				lgr.info('processing floor %s, quadrant %s' % (bldg_floor,
					floor_quadrant))

				# connect to the database
				cnxn, cursr = connect(options.db_driver, options.results_db_user,
					options.results_db_pwd, options.results_db, options.results_db_server)

				# fetch observed data
				observed_data_obj = get_observed_data(building_id, bldg_floor,
					floor_quadrant, options, lgr)

				# fetch predictions
				if options.feed_type == 'TPOSIF':
					prediction_data = get_prediction_data(cursr,
						bldg_floor, floor_quadrant, options, lgr)
				else:
					if options.bms != 'Schneider':
						prediction_data = get_prediction_data(cursr, bldg_floor,
							floor_quadrant, options, lgr)
					else:
						prediction_data = get_prediction_data_Schneider(cursr,
							bldg_floor, floor_quadrant, options, lgr)

				# compute scores
				scores = score_predictions(observed_data_obj.data,
					prediction_data, options, lgr)
				#lgr.info(scores)

				lgr.info('saving scores')
				save_scores(scores, cnxn, cursr, bldg_floor, floor_quadrant,
					options, lgr)

				# compute and deltas
				# prediction_deltas = utils.compute_deltas(prediction_data,
					# options, lgr)
				# observed_deltas = utils.compute_deltas(observed_data_obj.data,
					# options, lgr)
				# lgr.info('saving deltas')
				# save_deltas(prediction_deltas, observed_deltas, bldg_floor,
					# floor_quadrant, cursr, cnxn, options, lgr)

				# close connections
				cursr.close()
				cnxn.close()

		except Exception, e:
			lgr.critical('scoring %s failed: %s' % (building_id,
				traceback.format_exc()))

if __name__ == '__main__':
	main(sys.argv)