#!/bin/env python

import sys
import datetime

class Time_Covariates:

	def __init__(self, keys, holidays_obj, options, lgr):

		self.lgr = lgr
		self.options = options
		self.keys = keys
		self.holidays_obj = holidays_obj

		self.columns = ['hour', 'hour_of_day', 'day_of_wk',
			'weekend_id', 'oper_hour', 'occ_pct', 'no_oper_prev_day']

		self.covariates = self.gen_covariates()


	def gen_covariates(self):
		""" generate covariates """

		covariates = []

		for ts in self.keys:

			hour = ts.hour
			hour_of_day = ts.hour + ts.minute/60.0
			day_of_wk = ts.isoweekday()

			weekend_id = 0
			if day_of_wk == 6:
				weekend_id = 1
			elif day_of_wk == 7:
				weekend_id = 2

			oper_hour = 1
			if day_of_wk not in [6, 7] and \
			   hour >= self.options.building_open_hour and \
			   hour < self.options.building_close_hour:
				oper_hour = 2

			# cache miss
			dt = ts.date()
			is_hol, occ_pct = self.holidays_obj.is_holiday_dt(dt)

			# was building operated yesterday
			prev_dt = dt - datetime.timedelta(days=1)
			is_hol_prev_day, occ_pct_prev_day = self.holidays_obj.is_holiday_dt(prev_dt)
			no_oper_prev_day = 0
			if not weekend_id and not is_hol:
				if (is_hol_prev_day and occ_pct_prev_day < 0.4) or prev_dt.isoweekday() == 7:
					no_oper_prev_day = 1

			covariates.append([hour, hour_of_day, day_of_wk, weekend_id,
				oper_hour, occ_pct, no_oper_prev_day])

		#self.lgr.info(covariates)
		return covariates
