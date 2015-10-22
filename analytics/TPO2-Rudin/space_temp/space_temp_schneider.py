#!/bin/env python

""" get observed space temperature data of a control-zone
	where data is from Schneider's BMS
"""

__version__ = '$Id'
__author__ = 'agagneja@ccls.columbia.edu'
_module = 'space_temp_schneider'

from collections import OrderedDict
import datetime
import os
import traceback
import re
import math

from common_rudin.db_utils import connect
import common_rudin.utils as utils

space_temp_query = """
	SELECT DateTimeEDT, PointValue
	FROM [%s].dbo.[%s]
	WHERE PointName = 'SpaceTemp'
	AND Controller = ? AND SubController = ?
	AND PointValue > 0
	AND DateTimeEDT <= ?
	ORDER BY DateTimeEDT
"""



class Space_Temp_Schneider:
	""" process space temp data """

	def __init__(self, building_id, floor, quadrant, lgr, options,
			forecast_start_ts):

		self.lgr = lgr
		self.options = options
		self.floor = floor # controller
		self.quadrant = quadrant # sub-controller
		self.forecast_start_ts = forecast_start_ts

		# extract actual floor number
		floor_re = re.compile('\w+_(\d+)\w+')
		self.actual_floor = floor_re.match(quadrant).group(1);

		self.columns = ['space_temp']
		self.data, self.keys = self.get_data()
		self.data, self.keys = utils.interpolate_data2(self.data, options, lgr)
		# some of the datapoints in the data may be very close to each other
		# e.g. there may be 2 readings withing the same minute;
		# this can happen due to interpolation
		self.data, self.keys = utils.filter_data(self.data, forecast_start_ts,
									options, lgr)

		if self.options.debug is not None and self.options.debug == 1:
			utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_space_temp_%s_%s.csv' % (building_id, floor, quadrant)),
				['timestamp'].extend(self.columns))

		self.MAX_OBS_GAP = datetime.timedelta(minutes=30)
		self.validate_data()



	def validate_data(self):
		""" validate raw data """

		prev_ts = None
		for ts, _ in self.data.items():
			if prev_ts and ts - prev_ts > self.MAX_OBS_GAP:
				self.lgr.warning('space temp observations missing between %s and %s'
					% (prev_ts, ts))
			prev_ts = ts



	def get_data(self):
		""" get space temperature data from database
		"""

		# connect
		cnxn, cursr = connect(self.options.db_driver, self.options.db_user,
			self.options.db_pwd, self.options.building_db,
			self.options.building_db_server)

		query = space_temp_query % (self.options.building_db,
			self.options.space_temp_tablename_format)

		if self.options.debug is not None and self.options.debug == 1:
			self.lgr.info('executing %s' % query)

		cursr.execute(query, self.floor, self.quadrant, self.forecast_start_ts)

		data = OrderedDict([])
		keys = []

		for row in cursr.fetchall():
			ts, space_temp = row

			# filter based on required granularity
			# if ts.minute % self.options.forecast_granularity != 0:
				# continue

			# ignore seconds and microseconds
			# ts -= datetime.timedelta(seconds=ts.second,
				# microseconds=ts.microsecond)

			data[ts] = space_temp
			keys.append(ts)

		#self.lgr.info('first entry = %s' % data.items()[0])

		# close connection
		cursr.close()
		cnxn.close()

		return [data, keys]


	def save_predictions(self, run_ts, hour, labels, keys, sigma):
		""" save predictions to database """

		# validate key and label count
		if len(labels) != len(keys):
			lgr.critical('key count and label count must match. prediction save failed')
			sys.exit(1)

		insert_stmt = """
			INSERT INTO [%s] 
				(Run_DateTime, Prediction_DateTime, Floor, Controller,
				 SubController, Prediction_Value, Lower_Bound_95,
				 Upper_Bound_95, Lower_Bound_68, Upper_Bound_68)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		""" % (self.options.results_table)

		# connect to database
		cnxn, cursr = connect(self.options.db_driver, self.options.results_db_user,
			self.options.results_db_pwd, self.options.results_db,
			self.options.results_db_server)

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

			# floor = controller; quadrant = sub-controller
			row = (run_ts, ts, self.actual_floor, self.floor, self.quadrant,
				y_predict, lower_limit_95,
				y_predict + upper_bound_95 if sigma else None,
				lower_limit_68_2,
				y_predict + upper_bound_68_2 if sigma else None)

			insert_seq.append(row)

		try:
			cursr.executemany(insert_stmt, insert_seq)
		except Exception, e:
			self.lgr.critical('saving forecast to database failed: %s' %
				traceback.format_exc())

		cnxn.commit()
		cnxn.close()

