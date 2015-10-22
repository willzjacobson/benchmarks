#!/bin/env python

""" predict space temperature in a given quadrant of a given floor based on
	past observed load and other covariates
"""

__version__ = '$Id'
__author__ = 'agagneja@ccls.columbia.edu'
_module = 'electric_tenant'

from collections import OrderedDict
import datetime
import os
import sys
import numpy
import traceback

from common_rudin.db_utils import connect
import common_rudin.utils as utils

# constants
# SCHNEIDER_BMS = 'Schneider'

query_prefix = """
	SELECT t1.Timestamp, %s
	FROM """

# a floor can have more than one smart meter installed. If multiple meters are present,
# the query assumes that their data has the same timestamp
# We just sum the data from all equipment on the relevant floor
sub_query = """
	SELECT CONVERT(SMALLDATETIME, [TIMESTAMP]) TIMESTAMP, SUM(VALUE) VALUE
	FROM [%s].dbo.[%s]
	WHERE FLOOR = '%s' AND VALUE > 0
	GROUP BY CONVERT(SMALLDATETIME, [TIMESTAMP])
"""

floor_query = """
	SELECT CONVERT(SMALLDATETIME, [TIMESTAMP]) TIMESTAMP, SUM(VALUE) VALUE
	FROM (SELECT DISTINCT TIMESTAMP, FLOOR, VALUE FROM [%s].dbo.[%s]) t
	WHERE TIMESTAMP > ? AND TIMESTAMP < ? AND FLOOR = ? AND VALUE > 0
	GROUP BY CONVERT(SMALLDATETIME, [TIMESTAMP])
	ORDER BY TIMESTAMP
"""

where_clause = """ WHERE t1.TIMESTAMP > ? AND t1.TIMESTAMP < ?
	ORDER BY t1.TIMESTAMP
"""

query_suffix = """ t%d.Timestamp = t%d.Timestamp """


class Electric_Tenant:
	""" process space temp data """

	def __init__(self, lgr, options, forecast_start_ts, tenant_id):

		self.lgr = lgr
		self.options = options
		self.forecast_start_ts = forecast_start_ts
		self.tenant_id = tenant_id

		self.columns = ['electric_demand_tenant']
		self.data, self.keys = self.get_data()
		utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_electric_demand_tenant.csv' % tenant_id),
				['timestamp'].extend(self.columns))
		# self.data, self.keys = utils.interpolate_data2(self.data,
			# self.options, self.lgr)
		# self.data, self.keys = self.interp_regulrz_data(self.data)
		utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_electric_demand_raw.csv' % tenant_id),
				['timestamp'].extend(self.columns))
		self.data, self.keys = utils.filter_data(self.data,
			self.forecast_start_ts, self.options, self.lgr)

		if self.options.debug is not None and self.options.debug == 1:
			utils.write_dict_to_csv(self.data, os.path.join(
				self.options.temp_dir, '%s_electric_demand_filtered.csv' % tenant_id),
				['timestamp'].extend(self.columns))
		#sys.exit(0)

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

				# skip first line
				for line in f_in.readlines()[2:]:
					cols = line.split('\t')

					# strip whitespace
					cols = map(str.strip, cols)

					ts = datetime.datetime.strptime(cols[4] + ' ' + cols[8],
						'%m/%d/%Y %I:%M %p')

					# parse load value: may have commas, may end with a 
					# fullstop (.) and be surrounded by double quotes
					load = float(cols[10].strip('".').replace(',', ''))

					data[ts] = load
					#keys.append(ts)

		return [data, data.keys()]


	def get_data_old(self, floor):
		""" get steam demand data from database
		"""

		most_recent_csv_ts = datetime.datetime(1970, 1, 1, 0, 0)

		# get data from CSV
		data, keys = self.get_data_csv()
		if keys and len(keys):
			most_recent_csv_ts = keys[-1]

		#sys.exit(0)

		# get data from live feed from where the CSV left off
		# connect to db
		cnxn, cursr = connect(self.options.db_driver, self.options.db_user,
			self.options.db_pwd, self.options.tenant_db,
			self.options.tenant_db_server)

		tenant_floors = utils.parse_value_list(self.options.tenant_floors)
		query = ''
		if len(tenant_floors):
			query += sub_query % (self.options.tenant_db,
				self.options.electric_load_table, tenant_floors[0])

		#self.lgr.info('stage 1: %s' % query)
		self.lgr.info('tenant floors: %s' % tenant_floors)
		#on_clause = ''
		#if len(tenant_floors) > 1:
		query = '(' + query + ') t1 '
		#on_clause = ' ON '

		for i, tenant_floor in enumerate(tenant_floors[1:]):
			query += 'INNER JOIN (%s) t%d ON t1.Timestamp = t%d.Timestamp ' % (sub_query % (
				self.options.tenant_db, self.options.electric_load_table,
				tenant_floor), i+2, i+2)
			# if i > 0:
				# on_clause += 'AND'
			# on_clause += (' t1.Timestamp = t%d.Timestamp ' % (i + 2,))

		#if on_clause:
		sum_clauses = []
		for i, _ in enumerate(tenant_floors):
			sum_clauses.append('t%d.Value' % (i+1,))
		query = (query_prefix % ' + '.join(sum_clauses)) + query
		#query += on_clause
		query += where_clause

		# self.lgr.info(query)
		# sys.exit(0)
			
		# load_query = ''
		# if self.options.feed_type == 'TPOSIF':
			# load_query = electric_load_data_query_new
		# else:
			# load_query = electric_load_data_query
			# if self.options.bms == SCHNEIDER_BMS:
				# load_query = electric_load_data_query_schneider
			

		# query = load_query % (self.options.tenant_db,
			# self.options.electric_load_table)

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

		self.lgr.info('first entry: %s' % keys[0])
		# close connection
		cursr.close()
		cnxn.close()

		return [data, keys]


	def get_floor_data(self, tenant_floor, most_recent_csv_ts, cursr):
		""" get load data from database for floor
		"""

		query = floor_query % (self.options.tenant_db,
			self.options.electric_load_table)

		self.lgr.info('getting data for tenant floor: %s' % tenant_floor)

		# self.lgr.info(query)
		# sys.exit(0)

		if self.options.debug is not None and self.options.debug == 1:
			self.lgr.info('executing %s, %s' % (query, most_recent_csv_ts))

		cursr.execute(query, most_recent_csv_ts, self.forecast_start_ts,
			tenant_floor)

		floor_data = OrderedDict([])
		for row in cursr.fetchall():
			ts, electric_load = row
			floor_data[ts] = electric_load

		return floor_data
	


	def get_data(self):
		""" get electric load data from database for each tenant floor,
			regularize the data then add them. This is done this way instead of
			writing a query to obtain the total because the smart meter data for 
			different floors may come in with different time stamp especially 
			if the floors are located in different building zones
		"""

		most_recent_csv_ts = datetime.datetime(1970, 1, 1, 0, 0)

		# get data from CSV
		data, keys = self.get_data_csv()
		if keys and len(keys):
			most_recent_csv_ts = keys[-1]

		tenant_floors = utils.parse_value_list(self.options.tenant_floors)

		# floor_id => OrderedDict containing floor load data
		floor_data = {}
		
		if len(tenant_floors):

			cnxn, cursr = connect(self.options.db_driver, self.options.db_user,
				self.options.db_pwd, self.options.tenant_db,
				self.options.tenant_db_server)

			for tenant_floor in tenant_floors:
				floor_data[tenant_floor] = self.get_floor_data(tenant_floor,
					most_recent_csv_ts, cursr)
				
				if self.options.debug:
					utils.write_dict_to_csv(floor_data[tenant_floor], os.path.join(
						self.options.temp_dir, '%s_fl_%s_electric_demand.csv' % (self.tenant_id, tenant_floor)),
						['timestamp', 'data'])
	
				# regularize data
				floor_data[tenant_floor], _ = self.interp_regulrz_data(
					floor_data[tenant_floor])
				if self.options.debug:
					utils.write_dict_to_csv(floor_data[tenant_floor], os.path.join(
						self.options.temp_dir, '%s_fl_%s_electric_demand_interp.csv' % (self.tenant_id, tenant_floor)),
						['timestamp', 'data'])

			# sum load over all tenant floors
			data = self.get_total_tenant_load(data, floor_data, tenant_floors)
			self.save_tenant_data(data, cursr, cnxn)
			
			# close connection
			cursr.close()
			cnxn.close()

		return [data, data.keys()]
		
		

	def get_total_tenant_load(self, data, tenant_floor_load, tenant_floors):
		""" compute total tenant load data """
		
		#tenant_load = OrderedDict([])
		floor_count = len(tenant_floors)

		if not floor_count:
			return data

		if floor_count == 1:
			return tenant_floor_load[tenant_floors[0]]

		keys = tenant_floor_load[tenant_floors[0]].keys()
		max_min_data_start_ts = keys[0]
		min_max_end_ts = keys[-1]
		
		self.lgr.info('floor %s: start_ts = %s; end_ts = %s' % (
			tenant_floors[0], keys[0], keys[-1]))
		
		
		for tenant_floor in tenant_floors[1:]:
			keys = tenant_floor_load[tenant_floor].keys()
			self.lgr.info('floor %s: start_ts = %s; end_ts = %s' % (
				tenant_floor, keys[0], keys[-1]))

			max_min_data_start_ts	= max(max_min_data_start_ts, keys[0])
			min_max_end_ts 			= min(min_max_end_ts, keys[-1])

		self.lgr.info('max_min_start_ts = %s; min_max_end_ts = %s' % (
			max_min_data_start_ts, min_max_end_ts))

		tmp_ts = max_min_data_start_ts
		tmp_ts = utils.adjust_ts(tmp_ts, self.options.forecast_granularity,
			self.options, self.lgr)
		gap_td = datetime.timedelta(minutes=self.options.forecast_granularity)

		while tmp_ts <= min_max_end_ts:
			total_load = 0.0
			for tenant_floor in tenant_floors:
				try:
					total_load += tenant_floor_load[tenant_floor][tmp_ts]
				except KeyError:
					if self.options.debug:
						# self.lgr.warn('data for %s missing for floor %s' % (
							# tmp_ts, tenant_floor))
						total_load = None
						break
			
			if total_load:
				data[tmp_ts] = total_load
			tmp_ts += gap_td

		return data


	def save_tenant_data(self, data, cursr, cnxn):
		""" save aggregated tenant load data """

		if not self.options.save_tenant_data:
			self.lgr.info('skipping saving new tenant load data')
			return

		tenant_query = 'SELECT MAX([Timestamp]) FROM [%s].dbo.[%s]'

		# get latest timestamp from table
		cursr.execute(tenant_query % (self.options.tenant_db,
			self.options.electric_load_table_total))

		latest_db_ts = datetime.datetime(1970, 1, 1)
		for row in cursr.fetchall():
			if row[0]:
				latest_db_ts = row[0]

		self.lgr.info('newest timestamp in table: = %s' % latest_db_ts)

		insert_stmt = """
			INSERT INTO [%s].dbo.[%s] 
				(Timestamp, Usage_kW)
			VALUES (?, ?)
		""" % (self.options.tenant_db,
			self.options.electric_load_table_total)

		# loop through data and append newer data to the table
		insert_seq = []
		for ts, load in data.iteritems():
			if ts > latest_db_ts and load > 0.0001:
				insert_seq.append((ts, load))

		new_row_count = len(insert_seq)
		if new_row_count:
			self.lgr.info('appending %d new rows' % new_row_count)

			try:
				cursr.executemany(insert_stmt, insert_seq)
				cnxn.commit()
			except Exception, e:
				self.lgr.critical('An error occurred while generating model: %s' %
					traceback.format_exc())
		
		
	def interp_regulrz_data(self, data_dict):
		""" interpolate data and regularize: selectively fill small gaps """

		interp_data = OrderedDict([])
		TWO_HOURS = datetime.timedelta(hours=2)

		# we ignore small second and millisecond fields; so two readings
		# may actually be apart by upto 16 minutes and it should still be normal
		allowed_gap = datetime.timedelta(minutes=self.options.forecast_granularity)
		gap_td  = datetime.timedelta(minutes=self.options.forecast_granularity)

		self.lgr.info('interpolating and regularizing...')
		# if gap_td >= TWO_HOURS:
			# lgr.warning('data interpolation skipped. forecast granularity too large')
			# return [data_dict, data_dict.keys()]

		# find timestamps to interpolate data for
		prev_ts = None
		interp_keys = []
		idx_ts = None
		for ts in data_dict.keys():

			if prev_ts:
				tmp_gap = ts - prev_ts

				# if the observations are not aligned, regularize them
				# using interpolation
				idx_ts += gap_td
				if ts.minute != idx_ts.minute:
					interp_keys.append(idx_ts)

				#if tmp_gap > allowed_gap:
					#lgr.info('gap = %s; (%s, %s)' % (tmp_gap, prev_ts, ts))

				if tmp_gap > allowed_gap and tmp_gap <= TWO_HOURS:

					temp_ts = utils.adjust_ts(prev_ts, self.options.forecast_granularity,
						self.options, self.lgr)

					#lgr.info('adjusted prev ts: %s' % temp_ts)
					# adjusted prev_ts may be just prev_ts with seconds and milli-
					# second fields cleared
					if temp_ts <= prev_ts:
						temp_ts += gap_td
					#lgr.info('adjusted prev ts 2: %s' % temp_ts)

					#new_keys = []
					while temp_ts < ts and temp_ts > prev_ts:
						#new_keys.append(temp_ts)
						interp_keys.append(temp_ts)
						temp_ts += gap_td

					# update index ts so as not to regularize in large gaps
					idx_ts = utils.adjust_ts(ts, self.options.forecast_granularity,
						self.options, self.lgr)
					#lgr.info('new keys: %s' % new_keys)
			else:
				idx_ts = utils.adjust_ts(ts, self.options.forecast_granularity,
						self.options, self.lgr)

			prev_ts = ts

		# interpolate
		interp_values = None
		if len(interp_keys):
			#lgr.info('keys to interpolate: %s' % interp_keys)
			interp_values = numpy.interp(
				map(utils.ts_to_time_index, interp_keys),
				map(utils.ts_to_time_index, data_dict.keys()),
				data_dict.values(), None, None)

			# merge interpolated data and observed data 
			# lgr.info(len(interp_keys))
			# lgr.info(len(interp_values))
			tmp_dict = dict(data_dict.items() + zip(interp_keys, list(interp_values)))
			sorted_keys = sorted(tmp_dict.keys()) #, key=tmp_dict.__getitem__)
			for key in sorted_keys:
				interp_data[key] = tmp_dict[key]

		else:
			interp_data = data_dict
						
		return [interp_data, interp_data.keys()]
