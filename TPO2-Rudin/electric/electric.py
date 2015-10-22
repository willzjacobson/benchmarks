#!/bin/env python

""" predict space temperature in a given quadrant of a given floor based on
	past observed load and other covariates
"""

__version__ = '$Id'
__author__ = 'agagneja@ccls.columbia.edu'
_module = 'electric'

from collections import OrderedDict
import datetime
import os
import sys

from common_rudin.db_utils import connect
import common_rudin.utils as utils

# constants
SCHNEIDER_BMS = 'Schneider'


electric_load_data_query = """
	SELECT TIMESTAMP, VALUE
	FROM [%s].dbo.[%s]
	WHERE TIMESTAMP > ? AND TIMESTAMP < ? AND VALUE > 0
	ORDER BY TIMESTAMP
"""

electric_load_data_query_new = """
	SELECT CONVERT(SMALLDATETIME, [TIMESTAMP]) ts, SUM([VALUE]) load
	FROM (SELECT DISTINCT TIMESTAMP, EQUIPMENT_NO, VALUE FROM [%s].[dbo].[%s]) t
	WHERE [TIMESTAMP] > ? AND [TIMESTAMP] < ?
	GROUP BY CONVERT(SMALLDATETIME, [TIMESTAMP])
	ORDER BY ts
"""

electric_load_data_query_schneider = """
	SELECT DISTINCT DateTimeEDT, PointValue
	FROM [%s].dbo.[%s]
	WHERE DateTimeEDT > ? AND DateTimeEDT < ?
		AND PointName = 'KW.ALL' AND PointValue > 0
	ORDER BY DateTimeEDT
"""



class Electric:
	""" process space temp data """

	def __init__(self, lgr, options, forecast_start_ts, building_id):

		self.lgr = lgr
		self.options = options
		self.forecast_start_ts = forecast_start_ts

		self.columns = ['electric_demand']
		self.data, self.keys = self.get_data()
		utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_electric_demand_raw.csv' % building_id),
				['timestamp'].extend(self.columns))
		self.data, self.keys = utils.interpolate_data2(self.data,
			self.options, self.lgr)
		utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_electric_demand_interp.csv' % building_id),
				['timestamp'].extend(self.columns))
		self.data, self.keys = utils.filter_data(self.data,
			self.forecast_start_ts, self.options, self.lgr)

		if self.options.debug is not None and self.options.debug == 1:
			utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_electric_demand.csv' % building_id),
				['timestamp'].extend(self.columns))

		self.MAX_OBS_GAP = datetime.timedelta(minutes=30)
		self.validate_data()



	def validate_data(self):
		""" validate raw data """

		prev_ts = None
		for ts in self.data.keys():
			if prev_ts and ts - prev_ts > self.MAX_OBS_GAP:
				self.lgr.warning('electric demand observations missing between %s and %s'
					% (prev_ts, ts))
			prev_ts = ts



	def get_data_csv(self):
		""" get electric demand data from csv 
			assumption: data is chronologically ordered
		"""

		data = OrderedDict([])

		# use csv if one is available
		if self.options.electric_data_file and \
		   len(self.options.electric_data_file) > 0:
			with open(self.options.electric_data_file, 'r') as f_in:

				# skip first two lines
				for line in f_in.readlines()[2:]:
					cols = line.split('\t')

					# strip whitespace
					cols = map(str.strip, cols)

					# parse timestamp
					ts = datetime.datetime.strptime(cols[0], '%m/%d/%Y %H:%M')

					# moved to utils.filter_data()
					# filter based on required granularity
					# if ts.minute % self.options.forecast_granularity != 0:
						# continue

					# ignore seconds and microseconds
					# ts -= datetime.timedelta(seconds=ts.second,
						# microseconds=ts.microsecond)

					# parse load value: may have commas, may end with a 
					# fullstop (.) and be surrounded by double quotes
					try:
						load = float(cols[1].strip('"').rstrip('.').replace(',', ''))
					except ValueError as e:
							self.lgr.info('%s: %s' % (e.errno, e.strerror))

					data[ts] = load
					#keys.append(ts)

		return [data, data.keys()]


	def get_data(self):
		""" get steam demand data from database
		"""

		most_recent_csv_ts = datetime.datetime(1970, 1, 1, 0, 0)

		# get data from MACH Energy CSV
		#if self.options.building_id == 'Rudin_345Park':
		data, keys = self.get_data_csv()
		if keys and len(keys):
			most_recent_csv_ts = keys[-1]

		# get data from live feed from where the CSV left off
		# connect to db
		cnxn, cursr = connect(self.options.db_driver, self.options.db_user,
			self.options.db_pwd, self.options.building_db,
			self.options.building_db_server)

		load_query = ''
		if self.options.feed_type == 'TPOSIF':
			load_query = electric_load_data_query_new
		else:
			load_query = electric_load_data_query
			if self.options.bms == SCHNEIDER_BMS:
				load_query = electric_load_data_query_schneider
			

		query = load_query % (self.options.building_db,
			self.options.electric_load_table)

		if self.options.debug is not None and self.options.debug == 1:
			self.lgr.info('executing %s, %s' % (query, most_recent_csv_ts))

		cursr.execute(query, most_recent_csv_ts, self.forecast_start_ts)

		for row in cursr.fetchall():
			ts, electric_load = row

			# filter based on required granularity
			# if ts.minute % self.options.forecast_granularity != 0:
				# continue

			# ignore seconds and microseconds
			# ts -= datetime.timedelta(seconds=ts.second,
				# microseconds=ts.microsecond)

			data[ts] = electric_load
			keys.append(ts)

		#self.lgr.info('first entry: %s' % keys[0])
		# close connection
		cursr.close()
		cnxn.close()

		return [data, keys]