#!/bin/env python

""" predict space temperature in a given quadrant of a given floor based on
	past observed load and other covariates
"""

__version__ = '$Id'
__author__ = 'agagneja@ccls.columbia.edu'
_module = 'occupancy'

from collections import OrderedDict
import datetime
import os
import sys

from common_rudin.db_utils import connect
import common_rudin.utils as utils

# constants
SCHNEIDER_BMS = 'Schneider'


occupancy_query = """
	SELECT DISTINCT [TIMESTAMP], [VALUE]
	FROM [%s].[dbo].[%s]
	WHERE [TIMESTAMP] < ?
	ORDER BY [TIMESTAMP]
"""




class Occupancy:
	""" process space temp data """

	def __init__(self, lgr, options, forecast_start_ts, building_id):

		self.lgr = lgr
		self.options = options
		self.forecast_start_ts = forecast_start_ts

		self.columns = ['electric_demand']
		self.data, self.keys = self.get_data()
		utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_occupancy_raw.csv' % building_id),
				['timestamp'].extend(self.columns))

		# perform interpolation to fill small gaps
		self.data, self.keys = utils.interpolate_data2(self.data,
			self.options, self.lgr)
		utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_occupancy_interp.csv' % building_id),
				['timestamp'].extend(self.columns))

		
		self.data, self.keys = utils.filter_data(self.data,
			self.forecast_start_ts, self.options, self.lgr)
		if self.options.debug is not None and self.options.debug == 1:
			utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_occupancy_filtered.csv' % building_id),
				['timestamp'].extend(self.columns))

		self.MAX_OBS_GAP = datetime.timedelta(minutes=30)
		self.validate_data()



	def validate_data(self):
		""" validate raw data """

		prev_ts = None
		for ts in self.data.keys():
			if prev_ts and ts - prev_ts > self.MAX_OBS_GAP:
				self.lgr.warning('occupancy observations missing between %s and %s'
					% (prev_ts, ts))
			prev_ts = ts



	def get_data(self):
		""" get data from database
		"""

		# get data from live feed from where the CSV left off
		# connect to db
		cnxn, cursr = connect(self.options.db_driver, self.options.db_user,
			self.options.db_pwd, self.options.building_db,
			self.options.building_db_server)

		query = occupancy_query % (self.options.building_db,
			self.options.occupancy_table)

		if self.options.debug is not None and self.options.debug == 1:
			self.lgr.info('executing %s' % query)

		cursr.execute(query, self.forecast_start_ts)

		data = OrderedDict([])

		for row in cursr.fetchall():
			ts, value = row
			data[ts] = value


		if self.options.debug:
			self.lgr.info('%d rows fetched' % len(data))

		# close connection
		cursr.close()
		cnxn.close()

		return [data, data.keys()]