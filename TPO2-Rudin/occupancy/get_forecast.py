#!/bin/env python

""" get newer occupancy data
"""

__version__ = '$Id'
__author__ = 'ag2818@columbia.edu'
_module = 'get_forecast'

from collections import OrderedDict
import datetime
import os
import sys

from common_rudin.db_utils import connect
import common_rudin.utils as utils

occ_fcst_query = """
	SELECT t1.Prediction_DateTime, t1.Prediction_Value
	FROM [%s].[dbo].[%s] t1,
		(SELECT  MAX(Run_DateTime) Run_DateTime, Prediction_DateTime
			FROM [%s].[dbo].[%s]
			GROUP BY Prediction_DateTime) t2
	WHERE t1.Prediction_DateTime >= ?
		AND t1.Run_DateTime = t2.Run_DateTime
		AND t1.Prediction_DateTime = t2.Prediction_DateTime
	ORDER BY t1.Prediction_DateTime
"""


class Occupancy_Forecast_Lite:
	""" process occupancy data """

	def __init__(self, lgr, options, last_obs_ts, building_id):

		self.lgr = lgr
		self.options = options
		self.last_obs_ts = last_obs_ts

		self.data = self.get_data()
		if self.options.debug:
			utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_occupancy_forecast_raw.csv' % building_id),
				['timestamp', 'occupancy'])


	def get_data(self):
		""" get data from database
		"""

		# get data from live feed from where the CSV left off
		# connect to db
		cnxn, cursr = connect(self.options.db_driver, self.options.db_user,
			self.options.db_pwd, self.options.building_db,
			self.options.building_db_server)

		query = occ_fcst_query % (self.options.building_db,
			self.options.results_table_occupancy, self.options.building_db,
			self.options.results_table_occupancy)

		if self.options.debug is not None and self.options.debug == 1:
			self.lgr.info('executing %s' % query)

		cursr.execute(query, self.last_obs_ts)

		data = OrderedDict([])
		for row in cursr.fetchall():
			ts, value = row
			data[ts] = value

		self.lgr.info('%d rows fetched' % len(data))

		# close connection
		cursr.close()
		cnxn.close()

		return data