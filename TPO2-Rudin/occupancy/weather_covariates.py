#!/bin/env python

import sys
import datetime
import traceback

class Weather_Covariates:

	def __init__(self, keys, weather_obj, learn_from_days, options, lgr):

		self.lgr = lgr
		self.options = options
		self.keys = keys
		self.weather_obj = weather_obj
		self.learn_from_days = learn_from_days
		# lag, in hours, to use for computing similarity score
		self.sim_score_lag = 2

		self.columns = ['bldg_oper_min_temp', 'bldg_oper_max_temp',
			'bldg_oper_avg_temp']
		for day_suffix in ['_prev_day', '_prev_wk']:
			self.columns += [col + day_suffix for col in self.weather_obj.columns]
			self.columns += [ col + '_diff' + day_suffix for col in self.weather_obj.columns]

		self.covariates = self.gen_covariates()

		

	def gen_covariates(self):
		""" generate weather covariates """

		covariates = []
		# weather covariates are stay the same over a given day
		# so we use a cache to avoid recomputing them
		#covariate_cache = {}

		for ts in self.keys:
			dt = ts.date()

			# look in cache first
			#if dt in covariate_cache:
			#	covariates.append(covariate_cache[dt])
			#	continue

			# cache miss: iterate weather data/forecast for
			# buidling operation hours
			start_ts = datetime.datetime.combine(dt,
				datetime.time(self.options.building_open_hour))

			end_hour = 11
			if self.options.building_open_hour >= end_hour \
			   and self.options.building_close_hour <= self.options.building_open_hour + 1:
				end_hour = self.options.building_open_hour + 1

			# we have forecast for the next 36 hours only
			# end_ts = datetime.datetime.combine(dt,
				# datetime.time(self.options.building_close_hour))
			end_ts = datetime.datetime.combine(dt,
				datetime.time(end_hour))
			gap_td = datetime.timedelta(
				minutes=self.options.forecast_granularity)

			idx = start_ts
			min_temp, max_temp, avg_temp = 999999, -999999, None
			daily_temp_list = []
			while idx < end_ts:
				try:
					#temp = self.weather_obj.temp_regularized[idx]
					temp = self.weather_obj.regularized_data[
						self.weather_obj.TEMP_IDX][idx]
				except KeyError, e:
					self.lgr.critical('weather data missing for %s\n%s' % (idx,
						traceback.format_exc()))
					raise Exception('weather data missing')
					#sys.exit(1)

				min_temp = min(temp, min_temp)
				max_temp = max(temp, max_temp)
				daily_temp_list.append(temp)

				idx += gap_td

			list_length = len(daily_temp_list)
			if list_length > 0:
				avg_temp = sum(daily_temp_list)/list_length
			
			# humidex
			humidex_data = self.weather_obj.regularized_data[
				self.weather_obj.HUMIDEX_IDX]
			#humidex = self.weather_obj.humidex_regularized[ts];
			humidex = humidex_data[ts];
			
			ts_weather = self.weather_obj.covariates[ts]
			
			data = [min_temp, max_temp, avg_temp]
			
			tm = ts.time()
			for tmp_dt in self.learn_from_days[dt]:
				if tmp_dt:
					tmp_ts = datetime.datetime.combine(tmp_dt, tm)
					tmp_ts_weather = self.weather_obj.covariates[tmp_ts]
					tmp_diff_weather = [a - b for a, b in zip(
						tmp_ts_weather, ts_weather)]
					data.extend(tmp_ts_weather)
					data.extend(tmp_diff_weather)
				else:
					data.extend([None] * (2*len(ts_weather)))

			covariates.append(data)
			#covariate_cache[dt] = data

		return covariates