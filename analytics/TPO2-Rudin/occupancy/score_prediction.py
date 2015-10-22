#!/bin/env python

__version__ = '$Id'
__author__ = 'agagneja@ccls.columbia.edu'
_module = 'score_prediction_occupancy'

__doc__ = """ score occupancy predictions
				using observed data
		  """

import sys
from collections import OrderedDict
import math
import datetime

import optparse
import cfgparse

from common_rudin.db_utils import connect
from common_rudin.common import log_from_config, setup
import common_rudin.utils as utils


from occupancy import Occupancy


def get_observed_data(building_id, options, lgr):
	""" """

	now = datetime.datetime.now() #datetime.datetime(2099, 1, 1)

	data_obj = Occupancy(lgr, options, now, building_id)

	# lgr.info('observed data length: %d' % len(data_obj.data))
	# utils.write_dict_to_csv(data_obj.data, '%s_obs_data.csv' % building_id, ['ts', 'obs'])
	return data_obj.data


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

				# mape can be None if observed data is 0
				if mape:
					scores[pred_dt][MAPE].append(mape)

			else:
				# mape can be None if observed data is 0
				mape_list = []
				if mape:
					mape_list.append(mape)

				scores[pred_dt] = {MAE:[mae], MSE:[mse], MAPE:mape_list}

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


def save_scores(scores, cnxn, cursr, options, lgr):
	""" save scores """

	score_table = options.score_table_occupancy
	
	insert_stmt = """
		INSERT INTO [%s].dbo.[%s]
		(Prediction_Date, RMSE, MAE, MAPE)
		VALUES (?, ?, ?, ?)
	""" % (options.results_db, score_table)

	del_stmt = """DELETE FROM [%s].dbo.[%s] WHERE Prediction_Date = ?""" % (options.results_db,
			score_table)

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
			lgr.info(mape_list)
			mape = 100 * (sum(mape_list)/len(mape_list))

		insert_seq.append((datetime.datetime.combine(pred_dt,
			datetime.time(0)), rmse, mae, mape))

		# delete any existing score for this date
		cursr.execute(del_stmt, (datetime.datetime.combine(pred_dt,
				datetime.time(0))))

	# save new scores
	if len(insert_seq):
		cursr.executemany(insert_stmt, insert_seq)
		cnxn.commit()



def get_prediction_data(cursr, building_id, options, lgr):
	""" retrieve prediction data """

	results_table = options.results_table_occupancy
	
	select_qry = """
		SELECT t1.Prediction_DateTime, t1.Prediction_Value
		FROM [%s].[dbo].[%s] t1,
			(SELECT  MAX(Run_DateTime) Run_DateTime, Prediction_DateTime
			 FROM [%s].[dbo].[%s]
			 GROUP BY Prediction_DateTime) t2
		WHERE t1.Run_DateTime = t2.Run_DateTime
			AND t1.Prediction_DateTime = t2.Prediction_DateTime
		ORDER BY t1.Prediction_DateTime
	""" % (options.results_db, results_table, options.results_db,
		results_table)

	# lgr.info(select_qry)
	cursr.execute(select_qry)

	prediction_data = OrderedDict([])
	for row in cursr.fetchall():
		pred_ts, obs = row
		prediction_data[pred_ts] = obs

	# lgr.info('prediction data len: %d' % len(prediction_data))
	# utils.write_dict_to_csv(prediction_data, '%s_pred_data.csv' % building_id, ['ts', 'obs'])
	return prediction_data


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

		if bldg_idx != 0:
			reinstantiate_cparser = True
		options = utils.load_bldg_config(building_id, oparser, cparser, argv,
			options, lgr, reinstantiate_cparser)

		if not options.predict_occupancy:
			lgr.info('skipping building %s' % building_id)
			continue

		# connect to the database
		cnxn, cursr = connect(options.db_driver, options.results_db_user,
			options.results_db_pwd, options.results_db, options.results_db_server)

		# fetch observed data
		observed_data = get_observed_data(building_id, options, lgr)

		# fetch predictions
		prediction_data = get_prediction_data(cursr,
			building_id, options, lgr)

		# compute scores
		scores = score_predictions(observed_data, prediction_data,
			options, lgr)
		# lgr.info(scores)

		lgr.info('saving scores')
		save_scores(scores, cnxn, cursr, options, lgr)

		# close connections
		cursr.close()
		cnxn.close()


if __name__ == '__main__':
	main(sys.argv)