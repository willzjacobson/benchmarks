#!/bin/env python

from sets import Set
import datetime
from collections import OrderedDict
import sys
import os
import math
import numpy
from scipy.spatial.distance import euclidean

from common_rudin.db_utils import connect
import common_rudin.utils as utils
from common_rudin.WetBulb import WetBulb


class Weather:
	""" load weather data """

	def __init__(self, lgr, options, forecast_start_ts=None):

		self.weather_data_raw, self.weather_regularized = None, None
		self.options = options
		self.lgr = lgr
		self.wet_bulb = WetBulb()
		
		self.forecast_start_ts = forecast_start_ts
		self.similar_wetbulb_day_cache = {}
		self.cache_file = None
		self.new_cache_entries = []

		# id = None
		# try:
			# id = self.options.building_id
		# except Exception, e:
			# id = self.options.tenant_id
		# self.sim_humidx_day_cache_file_suffix = (
			# '_sim_humidx_cache_%s.p' % id)
		self.sim_humidx_day_cache_file_suffix = ('_%s_sim_wetbulb_cache.p' %
			self.options.weather_station_id)

		self.columns = ['temp', 'dew_pt', 'humidex', 'wind speed', 'wind dir',
			'wind chill', 'heat index', 'pressure', 'wet bulb']

		# load
		self.weather_data_raw = self.load_weather_new(forecast_start_ts)

		# indexes in raw data ( see load_weather() )
		self.TEMP_IDX, self.HUMIDEX_IDX, self.WETBULB_IDX = 0, 2, 8
		
		if self.options.debug is not None and self.options.debug == 1:
			utils.write_dict_to_csv(self.weather_data_raw,
				os.path.join(self.options.temp_dir, 'weather_data_raw.csv'),
				['timestamp'].extend(self.columns))
			

		# validate
		self.MAX_OBS_GAP = datetime.timedelta(hours=2)
		self.validate_data()

		# regularize
		self.INTERPOLATION_GRANULARITY = self.options.forecast_granularity
		#self.BASE_TS = datetime.datetime(2010, 1, 1)
		# self.humidex_regularized = self.regularize_data(
			# self.weather_data_raw.keys(),
			# self._get_raw_data(self.weather_data_raw.keys(), self.HUMIDEX_IDX))
		# keys = self.humidex_regularized.keys()
		# lgr.info('regularized weather date range: (%s, %s)' % (keys[0], keys[-1]))

		# regularize temp
		# self.temp_regularized = self.regularize_data(
			# self.weather_data_raw.keys(),
			# self._get_raw_data(self.weather_data_raw.keys(), self.TEMP_IDX))

		# regularize dew pt
		# self.dewpt_regularized = self.regularize_data(
			# self.weather_data_raw.keys(),
			# self._get_raw_data(self.weather_data_raw.keys(), self.DEWPT_IDX))

		# if self.options.debug is not None and self.options.debug == 1:
			# utils.write_dict_to_csv(self.humidex_regularized,
				# os.path.join(self.options.temp_dir, 'humidex_regularized.csv'),
				# ['timestamp'].extend(self.columns))

		self.regularized_data = {}
		self.covariates = self.gen_covariates()

		#self.lgr.info(self.humidex_regularized)


	# def getHumidex(self, temp, dewPt):
		# """ convert temperature and dew point values observed together to humidex """
		# dewPtKlvn = dewPt + 273.15
		# e = 6.112 * math.exp(5417.7530 * ((1/273.16) - (1/dewPtKlvn)));
		# return temp + (0.5555 * (e - 10.0));



	def gen_covariates(self):
		""" generate covariates """

		# generate regularized keys
		raw_keys = self.weather_data_raw.keys()
		interp_indices, regularized_keys = self.gen_regularized_keys(raw_keys)

		for ID in range(0, 9):
			self.regularized_data[ID] = self.interpolate_data(
				raw_keys, self._get_raw_data(raw_keys, ID),
				interp_indices, regularized_keys)

		# generate covariates
		covariates = {}
		for key in regularized_keys:
			row = []
			for ID in range(0, 9):
				row.append(self.regularized_data[ID][key])
			#row.append(self.wet_bulb.computebulb(row[0], row[1], row[7]))
			covariates[key] = row

		return covariates



	def validate_data(self):
		""" validate raw weather data """
		prev_ts = None

		for ts, _ in self.weather_data_raw.items():
			if prev_ts and ts - prev_ts > self.MAX_OBS_GAP:
				self.lgr.warning('weather data missing between %s and %s' % (prev_ts, ts))

			prev_ts = ts


		# check if weather data is available for the desired range
		# keys = self.weather_data_raw.keys()
		# start_ts, end_ts = keys[0], keys[-1]
		# reqd_start_ts, reqd_end_ts = self.keys[0], self.keys[-1]

		# if reqd_start_ts < start_ts or reqd_end_ts > end_ts:
			# self.lgr.critical('weather data must be available between %s and %s' % (
				# reqd_start_ts, reqd_end_ts))
			#sys.exit(1)



	def _get_raw_data(self, keys, idx):
		""" get humidex values from weather data """

		raw_data = []
		for key in keys:
			if key in self.weather_data_raw:
				raw_data.append(self.weather_data_raw[key][idx])
			else:
				raw_data.append(None)
		return raw_data



	def regularize_data(self, keys, data):
		""" interpolate weather data """

		#keys = self.weather_data_raw.keys()
		obs_time_idx_keys = map(utils.ts_to_time_index, keys)
		start_ts, end_ts = keys[0], keys[-1]

		start_ts = utils.adjust_ts(start_ts, self.INTERPOLATION_GRANULARITY,
			self.options, self.lgr)

		# generate regularized keys
		tmp_ts = start_ts
		interp_indices, interp_keys = [], []
		gap_td = datetime.timedelta(minutes=self.INTERPOLATION_GRANULARITY)
		while tmp_ts < end_ts:
			interp_keys.append(tmp_ts)
			interp_indices.append(utils.ts_to_time_index(tmp_ts))
			tmp_ts += gap_td

		# interpolate
		interp_data = numpy.interp(interp_indices, obs_time_idx_keys,
			data, None, None)

		regularized_data = OrderedDict(zip(interp_keys, interp_data))
		return regularized_data



	def gen_regularized_keys(self, actual_keys):
		""" generate regularized keys """

		#keys = self.weather_data_raw.keys()
		
		start_ts, end_ts = actual_keys[0], actual_keys[-1]

		start_ts = utils.adjust_ts(start_ts, self.INTERPOLATION_GRANULARITY,
			self.options, self.lgr)

		# generate regularized keys
		tmp_ts = start_ts
		interp_indices, interp_keys = [], []
		gap_td = datetime.timedelta(minutes=self.INTERPOLATION_GRANULARITY)
		while tmp_ts < end_ts:
			interp_keys.append(tmp_ts)
			interp_indices.append(utils.ts_to_time_index(tmp_ts))
			tmp_ts += gap_td
		
		return [interp_indices, interp_keys]



	def interpolate_data(self, keys, data, interp_indices, interp_keys):
		""" interpolate data """

		obs_time_idx_keys = map(utils.ts_to_time_index, keys)
		interp_data = numpy.interp(interp_indices, obs_time_idx_keys,
			data, None, None)

		regularized_data = OrderedDict(zip(interp_keys, interp_data))
		return regularized_data



	def load_weather(self, forecast_start_ts):

		""" get raw weather data from database
			cursr: pre-connected database cursor
			database: name of the database
			table: name of the table containing observed weather data
			forecast_table: name of the table containing forecasted weather data
			forecast_start_ts: forecast start datetime object. This determines
				the time as of which the observed weather data is trucated and
				the most recent forecast available at the time is used
		"""

		# no timestamp specified or don't-use-forecast flag set?
		# use as much observed data as available
		tmp_forecast_start_ts = forecast_start_ts
		if self.options.use_weather_forecast == 0 or forecast_start_ts is None:
			tmp_forecast_start_ts = datetime.datetime(2199, 1, 1)
		self.lgr.info('observed weather-data cutoff ts = %s' % tmp_forecast_start_ts)
		
		# connect
		cnxn, cursr = connect(self.options.db_driver,
			self.options.weather_db_user, self.options.weather_db_pwd,
			self.options.weather_db, self.options.weather_db_server)

		# windchilla and heatindexa are supposed to be never
		# 'not null' at the same time; it can either be hot or cold but
		# it can't be hot and cold at the same time
		query = """
		SELECT * FROM
		(SELECT DISTINCT
				CASE
				WHEN WindChillA > -900 THEN WindChillA
				WHEN HeatIndexA > -900 THEN HeatIndexA
				ELSE TempA
				END as TempA, DewPointA,
				dbo.Humidex(
					CASE
					WHEN WindChillA > -900 THEN WindChillA
					WHEN HeatIndexA > -900 THEN HeatIndexA
					ELSE TempA
					END, DewPointA) Humidex,
				Date
			FROM [%s]
			WHERE Date <= ? 
			AND TempA > -900 AND DewPointA > -900
		UNION
		SELECT DISTINCT
				CASE
				WHEN WindChillA > -900 THEN WindChillA
				WHEN HeatIndexA > -900 THEN HeatIndexA
				ELSE TempA
				END as TempA,
				DewA as DewPointA,
				dbo.Humidex(
					CASE
					WHEN WindChillA > -900 THEN WindChillA
					WHEN HeatIndexA > -900 THEN HeatIndexA
					ELSE TempA
					END, DewA) Humidex,
				Date
			FROM [%s]
			WHERE Fcst_Date = (SELECT MAX(Fcst_Date)
								FROM [%s]
								WHERE Fcst_Date <= ?)
			AND Date >= ?
			AND TempA > -900 AND DewA > -900) t
		ORDER BY Date
		""" % (self.options.weather_table, self.options.weather_forecast_table,
			self.options.weather_forecast_table)

		if self.options.debug and self.options.debug == 1:
			self.lgr.info('fetching weather: %s, %s' % (
				query, tmp_forecast_start_ts))

		cursr.execute(query, tmp_forecast_start_ts, tmp_forecast_start_ts,
			tmp_forecast_start_ts)
		weather_data = OrderedDict([])

		for row in cursr.fetchall():
			#self.lgr.info(row[3])
			edt_ts = None
			try:
				edt_ts = datetime.datetime.strptime(str(row[3]).encode('utf8')[:-8],
					'%Y-%m-%d %H:%M:%S')
			except ValueError:
				edt_ts = datetime.datetime.strptime(str(row[3]).encode('utf8'),
					'%Y-%m-%d %H:%M:%S')

			temp, dew_pt, humidex = row[0], row[1], row[2]
			weather_data[edt_ts] = [temp, dew_pt, humidex]

		cnxn.close()
		return weather_data


	def load_weather_new(self, forecast_start_ts):

		""" get raw weather data from database
			cursr: pre-connected database cursor
			database: name of the database
			table: name of the table containing observed weather data
			forecast_table: name of the table containing forecasted weather data
			forecast_start_ts: forecast start datetime object. This determines
				the time as of which the observed weather data is trucated and
				the most recent forecast available at the time is used
		"""

		# no timestamp specified or don't-use-forecast flag set?
		# use as much observed data as available
		tmp_forecast_start_ts = forecast_start_ts
		if self.options.use_weather_forecast == 0 or forecast_start_ts is None:
			tmp_forecast_start_ts = datetime.datetime(2199, 1, 1)
		self.lgr.info('observed weather-data cutoff ts = %s' % tmp_forecast_start_ts)
		
		# connect
		cnxn, cursr = connect(self.options.db_driver,
			self.options.weather_db_user, self.options.weather_db_pwd,
			self.options.weather_db, self.options.weather_db_server)

		# windchilla and heatindexa are supposed to be never
		# 'not null' at the same time; it can either be hot or cold but
		# it can't be hot and cold at the same time
		query = """
		SELECT * FROM
		(SELECT DISTINCT
				TempA, DewPointA, dbo.Humidex(TempA, DewPointA) Humidex,
				WindSpeedA, WindDir,
				CASE WHEN WindChillA > -900 THEN WindChillA ELSE 0 END WindChillA,
				CASE WHEN HeatIndexA > -900 THEN HeatIndexA ELSE 0 END HeatIndexA,
				PressureA, Date
			FROM [%s]
			WHERE Date <= ? 
			AND TempA > -900 AND DewPointA > -900 AND WindSpeedA > -900
			AND WindDir > -900 AND PressureA > -900
		UNION
		SELECT DISTINCT
				TempA, DewA as DewPointA,
				dbo.Humidex(TempA, DewA) Humidex,
				WSpeedA, WDir,
				CASE WHEN WindChillA > -900 THEN WindChillA ELSE 0 END WindChillA,
				CASE WHEN HeatIndexA > -900 THEN HeatIndexA ELSE 0 END HeatIndexA,
				MSLPA as PressureA, Date
			FROM [%s]
			WHERE Fcst_Date = (SELECT MAX(Fcst_Date)
								FROM [%s]
								WHERE Fcst_Date <= ?)
			AND Date >= ?
			AND TempA > -900 AND DewA > -900 AND WSpeedA > -900
			AND WDir > -900 AND MSLPA > -900) t
		ORDER BY Date
		""" % (self.options.weather_table, self.options.weather_forecast_table,
			self.options.weather_forecast_table)

		if self.options.debug and self.options.debug == 1:
			self.lgr.info('fetching weather: %s, %s' % (
				query, tmp_forecast_start_ts))

		cursr.execute(query, tmp_forecast_start_ts, tmp_forecast_start_ts,
			tmp_forecast_start_ts)
		weather_data = OrderedDict([])

		for row in cursr.fetchall():
			#self.lgr.info(row[3])
			edt_ts = None
			try:
				edt_ts = datetime.datetime.strptime(str(row[8]).encode('utf8')[:-8],
					'%Y-%m-%d %H:%M:%S')
			except ValueError:
				edt_ts = datetime.datetime.strptime(str(row[8]).encode('utf8'),
					'%Y-%m-%d %H:%M:%S')

			temp, dew_pt, humidex, wind_speed = row[0], row[1], row[2], row[3]
			wind_dir, wind_chill, heat_idx = row[4], row[5], row[6]
			pressure = row[7]
			wet_bulb_t = self.wet_bulb.computebulb(temp, dew_pt, pressure)
			weather_data[edt_ts] = [temp, dew_pt, humidex, wind_speed,
				wind_dir, wind_chill, heat_idx, pressure, wet_bulb_t]

		cnxn.close()
		return weather_data
		

	# def load_weather(self, forecast_start_ts):
		# """ load weather data from database. If forecast_start_ts is None,
			# don't use weather forecast data
		# """

		##connect
		# cnxn, cursr = connect(self.options.db_driver,
			# self.options.weather_db_user, self.options.weather_db_pwd,
			# self.options.weather_db, self.options.weather_db_server)

		# tmp_forecast_start_ts = None
		# if self.options.use_weather_forecast:
			# tmp_forecast_start_ts = forecast_start_ts
		# self.lgr.info('forecast start ts = %s' % tmp_forecast_start_ts)

		# weather_data_raw = get_raw_weather_data(cursr,
			# self.options.weather_db, self.options.weather_table,
			# self.options.weather_forecast_table, tmp_forecast_start_ts,
			# self.options, self.lgr)

		##lgr.info(self.weather_data_raw)
		# cnxn.close()
		# return weather_data_raw


	def _compute_longlist(self, dt):
		""" compute long list of days potentially similar to dt 
			weekdays may be paired with other weekdays, Saturdays with other
			Saturdays and Sundays with other Sundays
		"""
		long_list = []

		# weekdays may be paired with other weekdays, Saturdays with other
		# Saturdays and Sundays with other Sundays
		# TODO: handle holidays
		isoweekday = dt.isoweekday()

		# Monday through Friday
		permitted_dow_range = range(2, 5)
		if isoweekday not in permitted_dow_range:
			permitted_dow_range = [isoweekday]

		# recent past and from a year ago
		# long_list = [dt - datetime.timedelta(days=x) for x in range(
			# 1, self.options.training_radius)]
		# long_list += [dt - datetime.timedelta(
			# days = 365 + self.options.training_radius - x) for x in range(
			# 1, 2*self.options.training_radius)]

		# to include shoulder months in the search more effectively,
		# use 1 year and 30 days to look for a similar weather day
		filtered_long_list = []
		for i in range(1, 365 + 31):
			date = dt - datetime.timedelta(days=i)
			if date.isoweekday() in permitted_dow_range:
				filtered_long_list.append(date)

		# filtered_long_list = []
		# for date in long_list:
			# if date.isoweekday() in permitted_dow_range:
				# filtered_long_list.append(date)

		return filtered_long_list


	def _get_humidex_vector(self, dt):
		""" get humidex vector for date dt
			start counting 3 hours before the building opens
		"""
		start_ts = datetime.datetime.combine(dt, datetime.time(4))
		# key_list = [start_ts + datetime.timedelta(
			# minutes=self.options.forecast_granularity*x) for x in range(0,
			# (self.options.building_close_hour - (
			# self.options.building_open_hour - 3))*(60/self.options.forecast_granularity))]
		# use one reading an hour to begin with
		key_list = [start_ts + datetime.timedelta(
			hours=x) for x in range(0,
			(self.options.building_close_hour - (
			self.options.building_open_hour - 3)))]

		humidex_list = []
		for key in key_list:
			if key in self.humidex_regularized:
				humidex_list.append(self.humidex_regularized[key])
			else:
				return []

		return humidex_list


	def __del__(self):
		""" cleanup """
		# dump cache
		self.lgr.info('dumping cache %s: %d' % (self.cache_file,
			len(self.new_cache_entries)))
		if self.cache_file and len(self.new_cache_entries):
			utils.pickler(self.cache_file, self.similar_wetbulb_day_cache,
				self.lgr, self.options)



	def _get_wetbulb_vector(self, dt):
		""" get wetbulb vector for date dt
			start counting 3 hours before the building opens
		"""

		start_ts = datetime.datetime.combine(dt, datetime.time(4))
		# key_list = [start_ts + datetime.timedelta(
			# minutes=self.options.forecast_granularity*x) for x in range(0,
			# (self.options.building_close_hour - (
			# self.options.building_open_hour - 3))*(60/self.options.forecast_granularity))]
		# use one reading an hour to begin with
		key_list = [start_ts + datetime.timedelta(
			hours=x) for x in range(0,
			(self.options.building_close_hour - (
			self.options.building_open_hour - 3)))]

		wetbulb_list = []
		for key in key_list:
			# if key in self.humidex_regularized:
				# humidex_list.append(self.humidex_regularized[key])
			if key in self.regularized_data[self.WETBULB_IDX]:
				wetbulb_list.append(self.regularized_data[self.WETBULB_IDX][key])
			else:
				return []

		return wetbulb_list


	def compute_similar_weather_day_cache(self, keys, model_type):
		""" compute similar weather day cache based on
			wet-bulb from 4am through 7pm
		"""

		# load cache
		self.cache_file = model_type + self.sim_humidx_day_cache_file_suffix
		if (not (self.forecast_start_ts and self.forecast_start_ts.hour == 0
				and self.forecast_start_ts.day % 14 == 0)
		   and not len(self.similar_wetbulb_day_cache)):

			self.similar_wetbulb_day_cache = utils.unpickler(self.cache_file,
				self.similar_wetbulb_day_cache, self.lgr, self.options)
			self.lgr.info('*** %d entries loaded' % len(self.similar_wetbulb_day_cache))

		new_entries = []
			
		days = set([]);
		for key in keys:
			days.add(key.date())

		# date -> list of (date, euclidean distance) sorted by euclidean distance
		self.lgr.info('computing wet bulb similarity scores')
		for day in days:
		
			# lookup cache
			if day in self.similar_wetbulb_day_cache:
				continue
			new_entries.append(day)

			days_longlist = self._compute_longlist(day)
			day_wetbulb = self._get_wetbulb_vector(day)
			if not len(day_wetbulb):
				continue
			
			# find 2 most similar humidex days
			for dt in days_longlist:
				# compute and save similarity score between day and dt
				dt_wetbulb = self._get_wetbulb_vector(dt)
				if not len(dt_wetbulb):
					continue
				score = euclidean(day_wetbulb, dt_wetbulb)
				
				if day in self.similar_wetbulb_day_cache:
					self.similar_wetbulb_day_cache[day].append((dt, score))
				else:
					self.similar_wetbulb_day_cache[day] = [(dt, score)]

		# sort long list by score
		for day in new_entries: #self.similar_wetbulb_day_cache:
			self.similar_wetbulb_day_cache[day] = sorted(
				self.similar_wetbulb_day_cache[day], key=lambda t: t[1])

		self.new_cache_entries.extend(new_entries)
