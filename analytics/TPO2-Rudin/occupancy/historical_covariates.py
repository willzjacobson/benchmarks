#!/bin/env python

import sys
import datetime
import math

class Historical_Covariates:

	def __init__(self, keys, space_temp_obj, weather_obj, hour, model_type,
					holidays_obj, options, lgr):

		self.lgr = lgr
		self.options = options
		self.keys = keys
		self.space_temp_obj = space_temp_obj
		self.hour = hour
		self.model_type = model_type
		self.holidays_obj = holidays_obj
		self.weather_obj = weather_obj

		self.ONE_DAY  = datetime.timedelta(days=1)
		self.ONE_WEEK = datetime.timedelta(days=7)

		self.columns = ['day_ago_%s' % model_type,
			'prev_day_avg_%s' % model_type, 'prev_day_hour_avg_%s' % model_type,
			'wk_ago_%s' % model_type, 'prev_wk_avg_%s' % model_type,
			'prev_wk_hour_avg_%s' % model_type]

		#self.holiday_data = self.get_holiday_data()
		self.covariates, self.learn_from_days = self.gen_covariates_new()
		if self.options.debug:
			self.lgr.info('learn from days:')
			for k, v in self.learn_from_days.iteritems():
				self.lgr.info('%s: %s' % (k, v))



	def compute_average(self, start_dt, end_dt):
		""" compute average observation over [start_dt, end_dt)"""

		# generate time stamp from date
		midnight_tm = datetime.time(0, 0, 0, 0)
		start_ts = datetime.datetime.combine(start_dt, midnight_tm)
		end_ts   = datetime.datetime.combine(end_dt, midnight_tm)

		# try:
			# start_idx = self.space_temp_obj.keys.index(start_ts)
		# except ValueError, e:
			# if self.options.debug is not None and self.options.debug == 1:
				# self.lgr.warning('key not found: %s' % e)
			# return None

		sum, count, missing_count = 0.0, 0, 0
		#for key in self.space_temp_obj.keys[start_idx:]:
		key = start_ts
		td = datetime.timedelta(minutes=self.options.forecast_granularity)
		while key < end_ts:

			try:
				sum += self.space_temp_obj.data[key]
				count += 1
			except KeyError:
				missing_count += 1
			
			key += td

		# compute average if at least 80% data available
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
			# start_idx = self.space_temp_obj.keys.index(start_ts)
		# except ValueError, e:
			# if self.options.debug is not None and self.options.debug == 1:
				# self.lgr.warning('key not found: %s' % e)
			# return None

		sum, count, missing_count = 0.0, 0, 0
		# for key in self.space_temp_obj.keys[start_idx:]:
			# if key >= end_ts:
				# break
		key = start_ts
		td = datetime.timedelta(minutes=self.options.forecast_granularity)
		while key < end_ts:

			# filter: look at the data for model hour only 
			if key.hour != self.hour:
				key += td
				continue

			try:
				sum += self.space_temp_obj.data[key]
				count += 1
			except KeyError:
				missing_count += 1

			key += td

		# compute average
		if count and missing_count/(count + missing_count) < 0.2:
			return sum/count
		return None


	def find_week_ago_ts(self, ts, dt, wk_day, is_hol, hol_pct, sim_day_cache):
		"""
			week ago ts:
				case 1: today is not holiday. If last week is not holiday
						use data from a week ago otherwise keep going back
						in one week steps. If no match found in 3 steps,
						just use previous day ts

				case 2: today is a holiday. Look for a similar holiday in the past
					or if none found, use data from a recent Saturday
		"""
		wk_ago_ts = ts - self.ONE_WEEK
		wk_ago_ts_default = wk_ago_ts # default return value
		is_hol_wk_ago_dt, hol_pct_wk_ago = self.holidays_obj.is_holiday(
				wk_ago_ts)
		
		# case 1
		if not is_hol:

			# case 1a
			# do not select week-back timestamp if data missing
			if not is_hol_wk_ago_dt and wk_ago_ts in self.space_temp_obj.data:
				return wk_ago_ts

			else: # case 1b
				for i in range(1,4):
					wk_ago_ts = wk_ago_ts - self.ONE_WEEK
					is_hol_wk_ago_dt, _ = self.holidays_obj.is_holiday(
						wk_ago_ts)

					if (not is_hol_wk_ago_dt
					   and wk_ago_ts in self.space_temp_obj.data):
						return wk_ago_ts

			return wk_ago_ts_default # no match found, use prev_day_ts may be

		# to avoid an infinite loop
		MAX_TRIES, num_tries = 400, 0

		# case 2, is_hol == True
		while True:

			# go back until a similar-holiday is found or until tries
			# exceed max-allowed tries. similarity is measured by the
			# holiday_percent field in the holiday table
		
			if math.fabs(hol_pct_wk_ago - hol_pct) < 0.05:
				# make sure that data exists for holidays
				if wk_ago_ts in self.space_temp_obj.data:
					return wk_ago_ts

			if num_tries > MAX_TRIES:
				# look for a recent Saturday with available data
				for i in range(1,4):
					wk_ago_ts = (ts - (i-1)*self.ONE_WEEK) - datetime.timedelta(
						days=wk_day + 1)
					if wk_ago_ts in self.space_temp_obj.data:
						return wk_ago_ts

				return wk_ago_ts_default

			wk_ago_ts = wk_ago_ts - self.ONE_DAY
			is_hol_wk_ago, hol_pct_wk_ago = self.holidays_obj.is_holiday(
				wk_ago_ts)
			num_tries += 1

		return wk_ago_ts_default


	
	def find_week_ago_ts_new(self, ts, dt, wk_day, is_hol, hol_pct,
		sim_day_ts):
		"""
			week ago ts:
				case 1: today is not holiday. If last week is not holiday
						use data from a week ago otherwise keep going back
						in one week steps. If no match found in 3 steps,
						just use previous day ts

				case 2: today is a holiday. Look for a similar holiday in the past
					or if none found, use data from a recent Saturday
		"""
		wk_ago_ts = ts - self.ONE_WEEK
		wk_ago_ts_default = wk_ago_ts # default return value
		is_hol_wk_ago_dt, hol_pct_wk_ago = self.holidays_obj.is_holiday(
				wk_ago_ts)
		
		# case 1
		if not is_hol:

			# case 1a
			# do not select week-back timestamp if data missing
			if not is_hol_wk_ago_dt and wk_ago_ts in self.space_temp_obj.data:
				return wk_ago_ts

			else: # case 1b
				for i in range(1,4):
					wk_ago_ts = wk_ago_ts - self.ONE_WEEK
					is_hol_wk_ago_dt, _ = self.holidays_obj.is_holiday(
						wk_ago_ts)

					if (not is_hol_wk_ago_dt
					   and wk_ago_ts in self.space_temp_obj.data):
						return wk_ago_ts

			return wk_ago_ts_default # no match found, use prev_day_ts may be

		else:
			return sim_day_ts
	


	def find_day_ago_ts(self, ts, dt, wk_day, is_hol, hol_pct, wk_ago_ts):
		"""
			case 1: today is not a holiday. Check previous similar-business-day
				Mon, Fri, Sat, Sun are unique and are similar to the day a week
				ago only

			case 2: today is not a holiday: If previous similar-business-day was
				a holiday, just use the day a week ago
		"""

		day_ago_ts = ts - self.ONE_DAY

		if wk_day not in [1, 5, 6, 7]:
			if is_hol:
				day_ago_ts = wk_ago_ts

		else: # wk_day in [1, 5, 6, 7]
			# Mon, Fri, Sat, Sun are similar to a week ago
			day_ago_ts = wk_ago_ts

		return day_ago_ts



	def find_sim_day_ts(self, ts, dt, wk_day, is_hol, hol_pct, sim_day_cache):
		"""
			Find the most similar weather day with the following characteristics:
			Case 1: today is not a holiday: find the most similar weather day
				with which is also not a holiday and which is m-f if today is m-f
				sat if today is sat, sunday if today is sunday
			case 2: today is a holiday: find the most similar holiday
		"""

		time = ts.time()

		# look for a recent Saturday for which observations are available
		recent_sat_ts = None
		for i in range(1,4):
			tmp_ts = (ts - (i-1)*self.ONE_WEEK) - datetime.timedelta(
				days=wk_day + 1)
			if tmp_ts in self.space_temp_obj.data:
				recent_sat_ts = tmp_ts
	
		# most similar holiday seen so far; default Saturday
		similar_hol_ts = recent_sat_ts

		# difference between the occupancy on the most similar holiday
		# seen so far and that today(ts)
		similar_hol_diff_min = 100

		for i, row in enumerate(sim_day_cache):
			tmp_dt, score = row
			is_hol_tmp, hol_pct_tmp = self.holidays_obj.is_holiday_dt(tmp_dt)
			
			# case 1
			if not is_hol:
				if not is_hol_tmp:
					tmp_ts = datetime.datetime.combine(tmp_dt, time)
					if tmp_ts in self.space_temp_obj.data:
						return tmp_ts

			else: # case 2
				if is_hol_tmp:
	
					tmp_ts = datetime.datetime.combine(tmp_dt, time)
					hol_occ_pct_diff = math.fabs(hol_pct_tmp - hol_pct)

					# if the holiday occupancy is close enough, use that
					if hol_occ_pct_diff < 0.05:
						if tmp_ts in self.space_temp_obj.data:
							return tmp_ts
					else:
						if hol_occ_pct_diff < similar_hol_diff_min:
							if tmp_ts in self.space_temp_obj.data:
								similar_hol_ts = tmp_ts
								similar_hol_diff_min = hol_occ_pct_diff

		# is None if is_hol is false,
		# may be assigned a value if is_hol is true and the most
		# similar holiday found wasn't close enough
		return similar_hol_ts 



	def gen_covariates_new(self):
		""" compute covariates """

		covariates = []
		learn_from_days = {}

		for ts in self.keys:

			iso_weekday = ts.isoweekday()
			is_hol, hol_pct = self.holidays_obj.is_holiday(ts)
			dt = ts.date()

			# similar weather
			sim_day_cache = self.weather_obj.similar_wetbulb_day_cache[dt]
			sim_day_ts = self.find_sim_day_ts(ts, dt, iso_weekday, is_hol,
				hol_pct, sim_day_cache)

			# find previous day ts, previous week ts and most similar weather day ts
			week_ago_ts = self.find_week_ago_ts_new(ts, dt, iso_weekday, is_hol,
				hol_pct, sim_day_ts)
			# previous day
			day_ago_ts = self.find_day_ago_ts(ts, dt, iso_weekday, is_hol,
				hol_pct, week_ago_ts)

			if self.options.debug:
				self.lgr.info('ts: %s: %s, %s, %s' % (ts, day_ago_ts,
					week_ago_ts, sim_day_ts))
			# save learn from days to generate delta weather covariates
			# learn_from_days[ts.date()] = [day_ago_ts ? day_ago_ts.date() : None,
				# week_ago_ts ? week_ago_ts.date(): None,
				# sim_day_ts  ? sim_day_ts.date() : None]

			# gen covariates
			row = []
			learn_from_days[dt] = []
			for tmp_ts in [day_ago_ts, week_ago_ts]:
					
				tmp_day_avg, tmp_hour_avg = None, None
				tmp_ts_obs = None

				if tmp_ts:
					learn_from_days[dt].append(tmp_ts.date())

					if tmp_ts in self.space_temp_obj.data:
						tmp_ts_obs = self.space_temp_obj.data[tmp_ts]
					
						interval_strt_dt = tmp_ts.date()
						interval_end_dt = interval_strt_dt + self.ONE_DAY

						tmp_day_avg = self.compute_average(
							interval_strt_dt, interval_end_dt)
						tmp_hour_avg = self.compute_average_hour(
							interval_strt_dt, interval_end_dt)

				else:
					learn_from_days[dt].append(None)

				row.extend([tmp_ts_obs, tmp_day_avg, tmp_hour_avg])
			
			covariates.append(row)

		return [covariates, learn_from_days]


	def gen_covariates(self):
		""" compute covariates """

		covariates = []
		learn_from_days = {}

		for ts in self.keys:

			iso_weekday = ts.isoweekday()
			is_holiday, holiday_pct = self.holidays_obj.is_holiday(ts)

			# compute week ago space temp
			wk_ago_spc_temp = None
			wk_ago_ts = ts - self.ONE_WEEK

			# if ts is a holiday don't use a week ago, for now use a percentage;
			# if ts is not a holiday
			# and the day a week ago is, go back in one week steps
			# until a non-hoilday is found

			is_holiday_wk_ago_dt, holiday_pct_wk_ago = self.holidays_obj.is_holiday(wk_ago_ts)
			holiday_multiplier = 1.0
			base_load = 0.6 # TODO: move this to config file
			if self.model_type == 'occupancy':
				base_load = 0.1

			# to avoid an infinite loop
			max_tries = 400
			num_tries = 0

			if self.model_type != 'space_temp':

				# this is a loaded condition: it covers the following cases:
				# 1. holiday today but no holiday week ago
				# 2. no holiday today but holidat week ago
				# 3. holiday today and holiday week ago but
				# 	 holidays differ in expected occupancy
				if math.fabs(holiday_pct_wk_ago - holiday_pct) > 0.01:

					# holiday lookup indicates the type of lookup; finding
					# a similar (wrt occupancy) holiday is harder than finding a similar
					# weekday
					holiday_lookup = 0
					if is_holiday:
						holiday_lookup = 1

					wk_ago_ts = wk_ago_ts - (self.ONE_DAY if holiday_lookup else self.ONE_WEEK)

					# go back until a working day is found or until tries
					# exceed max-allowed tries
					is_holiday_tmp, holiday_pct_tmp = self.holidays_obj.is_holiday(
						wk_ago_ts)
					while is_holiday_tmp:
					
						num_tries += 1
						if num_tries > max_tries:
							wk_ago_ts = None
							break

						wk_ago_ts = wk_ago_ts - (self.ONE_DAY if holiday_lookup else self.ONE_WEEK)
						is_holiday_tmp, holiday_pct_tmp = self.holidays_obj.is_holiday(
							wk_ago_ts)

			else:
			
				# space temp; use last saturday as the guess-timate
				# for mon-fri only
				if is_holiday and iso_weekday < 6:
					# for mon-fri, isoweekday + 1 gives last sat
					wk_ago_ts = ts - datetime.timedelta(days=iso_weekday + 1)
				

			# guess-timate holiday load based on occupancy
			# base_load + user_driven_load = total_load
			# user_driven_load = (1 - pct_base_load/100)* occupancy_pct/100
			# assumption: the pct_holiday from Rudin is actually pct_occupancy
			if not wk_ago_ts:
				holiday_multiplier = base_load + holiday_pct*(1 - base_load)
				wk_ago_ts = ts - self.ONE_WEEK
					
			if wk_ago_ts in self.space_temp_obj.data:
				wk_ago_spc_temp = holiday_multiplier * self.space_temp_obj.data[wk_ago_ts]

			# compute day ago space temp
			day_ago_spc_temp = None
			# for Fri/Sat/Sun/Mon use week-ago observation; Mon=1, Sat=6 
			if iso_weekday not in [1, 5, 6, 7]:
				day_ago_ts = ts - self.ONE_DAY
				
				if self.model_type != 'space_temp' and is_holiday \
				   and math.fabs(holiday_pct_wk_ago - holiday_pct) > 0.01:
				    # (not is_holiday and is_holiday_wk_ago_dt) or
					# (is_holiday and not is_holiday_wk_ago_dt) or
					# (is_holiday and is_holiday_wk_ago_dt and holiday_pct_wk_ago != holiday_pct)
					day_ago_ts = wk_ago_ts

				if day_ago_ts in self.space_temp_obj.data:
					day_ago_spc_temp = self.space_temp_obj.data[day_ago_ts]

			else:
				day_ago_spc_temp = wk_ago_spc_temp

			# previous day avg space temp
			prev_day_avg_spc_temp = None
			# for Fri/Sat/Sun/Mon use week-ago observation; Mon=1, Sat=6
			if iso_weekday not in [1, 5, 6, 7]:
				day_ago_dt = day_ago_ts.date() #(ts - self.ONE_DAY).date()
			else:
				day_ago_dt = wk_ago_ts.date() #(ts - self.ONE_WEEK).date()

			learn_from_days[ts.date()] = [day_ago_dt, wk_ago_ts.date()]

			prev_day_avg_spc_temp = self.compute_average(
				day_ago_dt, day_ago_dt + self.ONE_DAY)

			# prev_day_hour_avg_spc_temp
			prev_day_hour_avg_spc_temp = self.compute_average_hour(
				day_ago_dt, day_ago_dt + self.ONE_DAY)

			# week ago average space temp
			prev_wk_avg_spc_temp = None
			interval_strt_dt = wk_ago_ts.date()
			interval_end_dt = interval_strt_dt + self.ONE_WEEK #ts.date() #datetime.timedelta(days=(iso_weekday - 1))
			# prev_wk_avg_spc_temp = self.compute_average(
				# interval_end_dt - self.ONE_WEEK, interval_end_dt)
			prev_wk_avg_spc_temp = self.compute_average_hour(
				interval_strt_dt, interval_end_dt)

			# prev_wk_hour_avg_spc_temp
			# prev_wk_hour_avg_spc_temp = self.compute_average_hour(
				# interval_end_dt - self.ONE_WEEK, interval_end_dt)
			prev_wk_hour_avg_spc_temp = self.compute_average_hour(
				interval_strt_dt, interval_end_dt)

			row = [day_ago_spc_temp, wk_ago_spc_temp,
				prev_day_avg_spc_temp, prev_wk_avg_spc_temp,
				prev_day_hour_avg_spc_temp, prev_wk_hour_avg_spc_temp]

			upd_row = []
			for x in row:
				# some elements may be missing/None
				upd_row.append(x * holiday_multiplier if x else x)
				
			covariates.append(upd_row)

		return [covariates, learn_from_days]
			