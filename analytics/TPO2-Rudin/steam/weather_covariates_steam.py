#!/bin/env python

import sys
import datetime
import traceback


class Weather_Covariates_Steam:

	def __init__(self, keys, weather_obj, options, lgr):

		self.lgr = lgr
		self.options = options
		self.keys = keys
		self.weather_obj = weather_obj

		# self.columns = ['humidex_sim_day', 'humidex_sim_day2',
			# 'humidex_sim_day_delta', 'humidex_sim_day2_delta',
			# 'bldg_oper_min_temp', 'bldg_oper_max_temp',
			# 'bldg_oper_avg_temp', 'bldg_oper_min_temp_sim_day_delta',
			# 'bldg_oper_max_temp_sim_day_delta',
			# 'bldg_oper_avg_temp_sim_day_delta',
			# 'bldg_oper_min_temp_sim_day2_delta',
			# 'bldg_oper_max_temp_sim_day2_delta',
			# 'bldg_oper_avg_temp_sim_day2_delta']

		self.columns = ['bldg_oper_min_temp', 'bldg_oper_max_temp',
			'bldg_oper_avg_temp', 'bldg_oper_min_temp_sim_day_delta',
			'bldg_oper_max_temp_sim_day_delta',
			'bldg_oper_avg_temp_sim_day_delta',
			'bldg_oper_min_temp_sim_day2_delta',
			'bldg_oper_max_temp_sim_day2_delta',
			'bldg_oper_avg_temp_sim_day2_delta']

		for day_suffix in ['_sim_day', '_sim_day2']:
			self.columns += [col + day_suffix for col in self.weather_obj.columns]
			self.columns += [ col + '_diff' + day_suffix for col in self.weather_obj.columns]

		self.covariates = self.gen_covariates()



	def _get_stats(self, data):
		""" compute min max and average """

		_min, _max, _avg = sys.maxint, -sys.maxint - 1, None
		length = len(data)
		if length:
			_avg = sum(data)/length
			_min, _max = min(data), max(data)

		return [_min, _max, _avg]



	def gen_covariates(self):
		""" generate weather covariates """

		covariates = []
		# weather covariates are stay the same over a given day
		# so we use a cache to avoid recomputing them
		#covariate_cache = {}

		for ts in self.keys:
			dt = ts.date()
			tm = ts.time()

			# cache miss: iterate weather data/forecast for
			# buidling operation hours
			start_tm = datetime.time(self.options.building_open_hour)
			ts = datetime.datetime.combine(dt, start_tm)
			
			end_tm = datetime.time(self.options.building_close_hour)
			#end_ts = datetime.datetime.combine(dt, end_tm)
			gap_td = datetime.timedelta(
				minutes=self.options.forecast_granularity)

			# most similar days
			sim_dt = self.weather_obj.similar_wetbulb_day_cache[dt][0][0]
			sim_dt2 = self.weather_obj.similar_wetbulb_day_cache[dt][1][0]

			sim_day_ts  = datetime.datetime.combine(sim_dt, tm)
			sim_day2_ts = datetime.datetime.combine(sim_dt2, tm)

			humidex_data = self.weather_obj.regularized_data[
				self.weather_obj.HUMIDEX_IDX]
			# ts_humidx       = self.weather_obj.humidex_regularized[ts] 
			# humidx_sim_day  = self.weather_obj.humidex_regularized[sim_day_ts]
			# humidx_sim_day2 = self.weather_obj.humidex_regularized[sim_day2_ts]
			# ts_humidx       = humidex_data[ts] 
			# humidx_sim_day  = humidex_data[sim_day_ts]
			# humidx_sim_day2 = humidex_data[sim_day2_ts]
			
			covariate_subset = []
			ts_weather = self.weather_obj.covariates[ts]
			for tmp_ts in [sim_day_ts, sim_day2_ts]:
				tmp_ts_weather = self.weather_obj.covariates[tmp_ts]
				tmp_diff_weather = [a - b for a, b in zip(
					tmp_ts_weather, ts_weather)]
				covariate_subset.extend(tmp_ts_weather)
				covariate_subset.extend(tmp_diff_weather)

			idx = start_tm
			temp_list, sim_day_temp_list, sim_day2_temp_list = [], [], []
			temp_data = self.weather_obj.regularized_data[
				self.weather_obj.TEMP_IDX]
			while idx < end_tm:

				tmp_ts = datetime.datetime.combine(dt, idx)
				tmp_sim_day_ts = datetime.datetime.combine(sim_dt, idx)
				tmp_sim_day2_ts = datetime.datetime.combine(sim_dt2, idx)

				try:
					# temp = self.weather_obj.temp_regularized[tmp_ts]
					# tmp_sim_day = self.weather_obj.temp_regularized[tmp_sim_day_ts]
					# tmp_sim_day2 = self.weather_obj.temp_regularized[tmp_sim_day2_ts]
					temp = temp_data[tmp_ts]
					tmp_sim_day = temp_data[tmp_sim_day_ts]
					tmp_sim_day2 = temp_data[tmp_sim_day2_ts]
				except KeyError, e:
					self.lgr.critical('weather data missing for %s\n%s' % (idx,
						traceback.format_exc()))
					raise
					#sys.exit(1)

				temp_list.append(temp)
				sim_day_temp_list.append(tmp_sim_day)
				sim_day2_temp_list.append(tmp_sim_day2)

				idx = (tmp_ts + gap_td).time()


			min_temp, max_temp, avg_temp = self._get_stats(temp_list)
			min_temp_sim_day, max_temp_sim_day, avg_temp_sim_day = \
				self._get_stats(sim_day_temp_list)
			min_temp_sim_day2, max_temp_sim_day2, avg_temp_sim_day2 = \
				self._get_stats(sim_day2_temp_list)

			# data = [humidx_sim_day, humidx_sim_day2,
				# humidx_sim_day - ts_humidx, humidx_sim_day2 - ts_humidx,
				# min_temp, max_temp, avg_temp, min_temp_sim_day - min_temp,
				# max_temp_sim_day - max_temp, avg_temp_sim_day - avg_temp,
				# min_temp_sim_day2 - min_temp, max_temp_sim_day2 - max_temp,
				# avg_temp_sim_day2 - avg_temp]
			
			data = [min_temp, max_temp, avg_temp, min_temp_sim_day - min_temp,
				max_temp_sim_day - max_temp, avg_temp_sim_day - avg_temp,
				min_temp_sim_day2 - min_temp, max_temp_sim_day2 - max_temp,
				avg_temp_sim_day2 - avg_temp]
			data.extend(covariate_subset)
			

			covariates.append(data)
			#covariate_cache[dt] = data

		return covariates