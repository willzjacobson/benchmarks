#!/bin/env python

import sys
import datetime
import math

from common_rudin.db_utils import connect

class Holidays:

	def __init__(self, options, lgr):
		""" init holidays object """

		self.lgr = lgr
		self.options = options
		self.ONE_DAY  = datetime.timedelta(days=1)
		self.low_occupancy_day_cache = {}

		self.holidays = self.get_holiday_data()


	def get_holiday_data(self):
		""" read holiday information from db """

		# connect
		cnxn, cursr = None, None
		db = None
		try:
			cnxn, cursr = connect(self.options.db_driver, self.options.db_user,
				self.options.db_pwd, self.options.building_db,
				self.options.building_db_server)
			db = self.options.building_db
		except AttributeError:
			cnxn, cursr = connect(self.options.db_driver, self.options.db_user,
				self.options.db_pwd, self.options.tenant_db,
				self.options.tenant_db_server)
			db = self.options.tenant_db
			
		holiday_data = {}
		
		if not self.options.holiday_table:
			self.lgr.info('*** no holiday table specified ***')
			return holiday_data
		
		query = """
			SELECT DISTINCT Date, Percent_holiday FROM [%s].dbo.[%s]
			""" % (db, self.options.holiday_table)

		cursr.execute(query)

		for row in cursr.fetchall():
			dt, percent_holiday = row
			holiday_data[dt.date()] = percent_holiday

		self.lgr.info('%d holidays read' % len(holiday_data))

		cnxn.close()
		return holiday_data

			
	def is_holiday(self, ts):
		""" returns True is timestamp ts falls on a holiday, False otherwise
			weekends are not considered holidays and are handled differently
		"""

		# holiday percent is actually percent expected occupancy
		dt = ts.date()
		if dt in self.holidays:
			return (True, self.holidays[dt]/100.0)

		# check for days around holidays
		# check for days around holidays
		is_low_exp_occ_day, hol_pct = self.is_low_occupancy_day(ts.date())
		if is_low_exp_occ_day:
			return (True, hol_pct)
		
		return (False, 1.0) # 1.0 = 100%/normal expected occupancy


	def is_low_occupancy_day(self, dt):
		""" return true is dt is the last working day before a long weekend
			returns true if dt is the day before a holiday
			return true for the Saturdays of a long weekend since they are
			typically different from other Saturdays
		"""
		
		wk_day = dt.isoweekday()

		tmp_dt = dt + self.ONE_DAY
		holiday_count = 0
		holiday_dt = None
		WEEKEND = [6, 7]
		
		# increment dt till the next working day is found
		while (tmp_dt in self.holidays or tmp_dt.isoweekday() in WEEKEND):
			if tmp_dt in self.holidays:
				holiday_dt = tmp_dt
			holiday_count += 1
			tmp_dt += self.ONE_DAY

		# estimated occupancy on a low occupancy day
		estimated_occupancy = 0.60

		# if it is the last working day before a long weekend 
		if holiday_count >= 3:
			self.low_occupancy_day_cache[dt] = estimated_occupancy
			return [True, estimated_occupancy]
		
		# if tomorrow is a holiday, today's occupancy is expected to be low
		if holiday_count == 1 and holiday_dt:
			self.low_occupancy_day_cache[dt] = estimated_occupancy
			return [True, estimated_occupancy]
		
		# decrement dt till the next working day is found
		# holiday_count = 0
		# holiday_dt = None
		# tmp_dt = dt - self.ONE_DAY
		# while tmp_dt in self.holidays:
			# holiday_dt = tmp_dt
			# holiday_count += 1
			# tmp_dt -= 1

		# if yesterday was a holiday which was not part of a long weekend,
		# occupancy may be low today
		# if holiday_count == 1 and holiday_dt:
			# self.low_occupancy_day_cache[dt] = estimated_occupancy
			# return [True, estimated_occupancy]
		
		return [False, 1.0]



	def is_holiday_dt(self, dt):
		""" returns True is date dt falls is a holiday, False otherwise
			weekends are not considered holidays and are handled elsewhere
		"""

		if dt in self.holidays:
			return (True, self.holidays[dt]/100.0)
		
		# check for days around holidays
		is_low_exp_occ_day, hol_pct = self.is_low_occupancy_day(dt)
		if is_low_exp_occ_day:
			return (True, hol_pct)
		
		return (False, 1.0) # 1.0 = 100%/normal expected occupancy
