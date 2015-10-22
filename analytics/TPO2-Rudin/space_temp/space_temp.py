#!/bin/env python

""" get observed space temperature data of a control-zone
"""

__version__ = '$Id'
__author__ = 'agagneja@ccls.columbia.edu'
_module = 'space_temp'

from collections import OrderedDict
import datetime
import os

from common_rudin.db_utils import connect
import common_rudin.utils as utils

space_temp_query = """
	SELECT TIMESTAMP, VALUE
	FROM [%s].dbo.[%s]
	WHERE STATUS_TAG = '{ok}' AND TIMESTAMP < ?
	ORDER BY TIMESTAMP
"""

# space_temp_qry_new = """
	# SELECT CONVERT(SMALLDATETIME, [TIMESTAMP]) ts, SUM([VALUE]) load
	# FROM [%s].[dbo].[%s]
	# WHERE FLOOR = '%s' AND QUADRANT = '%s' AND [TIMESTAMP] < ?
	# GROUP BY CONVERT(SMALLDATETIME, [TIMESTAMP])
	# ORDER BY ts
# """

space_temp_qry_new = """
	SELECT DISTINCT CONVERT(SMALLDATETIME, [TIMESTAMP]) ts, [VALUE] load
	FROM [%s].[dbo].[%s]
	WHERE FLOOR = '%s' AND QUADRANT = '%s' AND [TIMESTAMP] < ?
	ORDER BY ts
"""



class Space_Temp:
	""" process space temp data """

	def __init__(self, building_id, floor, quadrant, lgr, options,
			forecast_start_ts):

		self.lgr = lgr
		self.options = options
		self.floor = floor
		self.quadrant = quadrant
		self.forecast_start_ts = forecast_start_ts

		self.columns = ['space_temp']
		self.data, self.keys = self.get_data()
		self.data, self.keys = utils.interpolate_data2(self.data, options, lgr)
		self.data, self.keys = utils.filter_data(self.data, forecast_start_ts,
									options, lgr)

		if self.options.debug is not None and self.options.debug == 1:
			utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_space_temp_%s_%s.csv' % (
				building_id, floor, quadrant)),
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

		query = None
		if self.options.feed_type == 'TPOSIF':
			query = space_temp_qry_new % (self.options.building_db,
				self.options.space_temp_tablename_format, self.floor,
				self.quadrant)
		else:
			query = space_temp_query % (self.options.building_db,
				self.options.space_temp_tablename_format % (self.floor,
				self.quadrant))

		if self.options.debug is not None and self.options.debug == 1:
			self.lgr.info('executing %s' % query)

		cursr.execute(query, self.forecast_start_ts)

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

		#lgr.info('first entry = %s' % self.data.items())

		# close connection
		cursr.close()
		cnxn.close()

		return [data, keys]