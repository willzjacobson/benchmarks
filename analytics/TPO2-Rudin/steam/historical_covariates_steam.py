#!/bin/env python

import sys
import datetime

import common_rudin.utils as utils


class Historical_Covariates_Steam:

	def __init__(self, keys, obs_data_obj, weather_obj, hour, model_type,
			holidays_obj, options, lgr):

		self.lgr = lgr
		self.options = options
		self.keys = keys
		self.obs_data_obj = obs_data_obj
		self.weather_obj = weather_obj

		self.hour = hour
		self.model_type = model_type
		self.holidays_obj = holidays_obj

		self.ONE_DAY  = datetime.timedelta(days=1)

		self.columns = ['sim_day_%s' % model_type, 'sim_day2_%s' % model_type,
			#'sim_day_avg_%s' % model_type, 'sim_day2_avg_%s' % model_type,
			'sim_day_hour_avg_%s' % model_type,
			'sim_day2_hour_avg_%s' % model_type]
		self.covariates = self.gen_covariates()


	def compute_average(self, start_dt, end_dt):
		""" compute average space temp over [start_dt, end_dt)"""
		# generate time stamp from date
		midnight_tm = datetime.time(0, 0, 0, 0)
		start_ts = datetime.datetime.combine(start_dt, midnight_tm)
		end_ts   = datetime.datetime.combine(end_dt, midnight_tm)

		# try:
			# start_idx = self.obs_data_obj.data.index(start_ts)
		# except ValueError, e:
			# if self.options.debug is not None and self.options.debug == 1:
				# self.lgr.warning('key not found: %s' % e)
			# return None

		sum, count, missing_count = 0.0, 0, 0
		# for key in self.obs_data_obj.keys[start_idx:]:
			# if key >= end_ts:
				# break

			# sum   += self.obs_data_obj.data[key]
			# count += 1
			
		tmp_ts = start_ts
		gap_td = datetime.timedelta(minutes=self.options.forecast_granularity)
		while tmp_ts < end_ts:
			if tmp_ts in self.obs_data_obj.data:
				try:
					sum += self.obs_data_obj.data[tmp_ts]
					count += 1
				except KeyError:
					missing_count += 1

			tmp_ts += gap_td

		# compute average
		if count and missing_count/(count + missing_count) < 0.2:
			return sum/count
		return None


	def compute_average_hour(self, start_dt, end_dt):
		""" compute average space temp over [start_dt, end_dt)"""
		# generate time stamp from date
		start_tm = datetime.time(self.hour, 0, 0, 0)
		start_ts = datetime.datetime.combine(start_dt, start_tm)
		end_ts   = datetime.datetime.combine(end_dt, start_tm)

		# try:
			# start_idx = self.obs_data_obj.keys.index(start_ts)
		# except ValueError, e:
			# if self.options.debug is not None and self.options.debug == 1:
				# self.lgr.warning('key not found: %s' % e)
			# return None

		sum, count, missing_count = 0.0, 0, 0
		# for key in self.obs_data_obj.keys[start_idx:]:
			# if key >= end_ts:
				# break

			##filter: look at the data for model hour only 
			# if key.hour != self.hour:
				# continue

			# sum   += self.obs_data_obj.data[key]
			# count += 1

		tmp_ts = start_ts
		gap_td = datetime.timedelta(minutes=self.options.forecast_granularity)
		while tmp_ts < end_ts:

			if tmp_ts.hour > self.hour or tmp_ts >= end_ts:
				break

			if tmp_ts.hour != self.hour:
				tmp_ts += gap_td
				continue

			if tmp_ts in self.obs_data_obj.data:
				try:
					sum += self.obs_data_obj.data[tmp_ts]
					count += 1
				except KeyError:
					missing_count += 1

			tmp_ts += gap_td

		# compute average
		if count and missing_count/(count + missing_count) < 0.2:
			return sum/count
		return None


	def find_next_non_holiday(self, start_idx, similar_weather_day_cache):
		""" find next most similar weather non-holiday for which
			data/observations are available
		"""

		for i, row in enumerate(similar_weather_day_cache):
			
			if i < start_idx:
				continue

			tmp_dt, _ = row
			is_holiday, _ = self.holidays_obj.is_holiday_dt(tmp_dt)
			obs_available = utils.check_obs_avlblty(tmp_dt,
				self.obs_data_obj, self.options, self.lgr)

			if obs_available and not is_holiday:
				return [tmp_dt, i + 1]
	
		return [None, None]



	def gen_covariates(self):
		""" compute covariates """

		covariates = []
		debug_dt = datetime.date(2013, 5, 14)
		
		holidays = self.holidays_obj.holidays

		for ts in self.keys:

			dt = ts.date()
			tm = ts.time()

			is_holiday, holiday_pct = self.holidays_obj.is_holiday_dt(dt)
			# it is not possible to learn from previous year holiday steam usage
			# and/or similar expected occupancy holiday since weather drives
			# steam usage in a big way and weather may be very different
			# on the above mentioned days compared to the forecast
			# for tomorrow so we use a multiplying factor based on
			# expected occupancy
			holiday_multiplier = 1.00

			base_load = 0.1
			if is_holiday:
				# assumption: holiday pct from Rudin is actually occupancy percent
				holiday_multiplier = base_load + (1 - base_load) * holiday_pct

			# similar-weather days
			tmp_idx = 0
			similar_day_cache = self.weather_obj.similar_wetbulb_day_cache[dt]
			sim_dt, tmp_idx = self.find_next_non_holiday(tmp_idx,
								similar_day_cache)

			# if a similar day is not found, skip to next key as
			# this one is hopeless
			if sim_dt is None:
				covariates.append([None]*len(self.columns))
				continue

			sim_dt2, tmp_idx = self.find_next_non_holiday(tmp_idx,
								similar_day_cache)

			if sim_dt2 is None:
				covariates.append([None]*len(self.columns))
				continue
			# sim_dt = self.weather_obj.similar_humidex_day_cache[dt][0][0]
			# sim_dt2 = self.weather_obj.similar_humidex_day_cache[dt][1][0]

			iso_weekday = ts.isoweekday()

			# compute similar-weather-day2 observed data
			sim_day2_obs = None
			sim_day2_ts = datetime.datetime.combine(sim_dt2, tm)
			if sim_day2_ts in self.obs_data_obj.data:
				sim_day2_obs = self.obs_data_obj.data[sim_day2_ts]

			# compute similar observation
			sim_day_obs = None
			sim_day_ts = datetime.datetime.combine(sim_dt, tm)
			if sim_day_ts in self.obs_data_obj.data:
				sim_day_obs = self.obs_data_obj.data[sim_day_ts]

			# previous day average space temp
			#sim_day_avg_obs = None
			# sim_day_avg_obs = self.compute_average(sim_dt,
				# sim_dt + self.ONE_DAY)

			# similar_day_hour_avg_spc_temp
			sim_day_hour_avg_obs = self.compute_average_hour(sim_dt,
				sim_dt + self.ONE_DAY)

			# previous week average space temp
			# sim_day2_avg_obs = None
			interval_end_dt = sim_dt2 + self.ONE_DAY
			# sim_day2_avg_obs = self.compute_average(
				# sim_dt2, interval_end_dt)

			# prev_wk_hour_avg_spc_temp
			sim_day2_hour_avg_obs = self.compute_average_hour(
				sim_dt2, interval_end_dt)

			if self.options.debug: #dt == debug_dt:
				self.lgr.info('ts: %s,sim dt: %s, sim dt2: %s' % (
					ts, sim_dt, sim_dt2))
				#sys.exit(0)

			cov_list = [sim_day_obs, sim_day2_obs, sim_day_hour_avg_obs,
					sim_day2_hour_avg_obs]

			# use holiday multiplier
			upd_cov_list = []
			for x in cov_list:
				# some elements may be missing/None
				upd_cov_list.append(x * holiday_multiplier if x else x)

			covariates.append(upd_cov_list)

		return covariates
			