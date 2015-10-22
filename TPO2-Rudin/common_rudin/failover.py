#!/bin/env python

import sys
import datetime
import math

from common_rudin.db_utils import connect
import traceback

class Failover:

	def __init__(self, hour, forecast_start_ts, run_ts, model_type,
		sign_prog, options, lgr):
		""" init failover object """

		self.lgr = lgr
		self.options = options
		self.forecast_start_ts = forecast_start_ts
		self.run_ts = run_ts
		self.sign_prog = sign_prog
		self.model_type = model_type
		
		self.id = None
		try:
			self.id = options.building_id
		except AttributeError:
			self.id = options.tenant_id
		
		self.keys = None
		if hour is not None:
			self.keys = self.gen_failover_keys(hour, forecast_start_ts)



	def check_obs_avlblty(self, dt, obs_obj):
		""" returns True if observations are available for times of day specified
			by failed_keys on date dt, False otherwise
		"""

		found = True
		observations = []

		for key in self.keys:
			# check if ts with similar-weather-date dt is available in observations
			tmp_key = datetime.datetime.combine(dt, key.time())

			if tmp_key not in obs_obj.data:
				found = False
				break
			else:
				observations.append(obs_obj.data[tmp_key])

		return [found, observations]



	def day_of_week_type(self, dow):
		""" WEEKDAYS = range(1, 6)
			SATURDAY = [6]
			SUNDAY   = [7]
		"""

		category = 'WEEKDAY'
		if dow == 6:
			category = 'SATURDAY'
		elif dow == 7:
			category = 'SUNDAY'

		return category

	
	
	def find_best_failover(self, similar_weather_days, dt,
			obs_obj, holidays_obj):
		""" find best failover observations for the failed keys
			model_types:
				steam, electric, tenant_electric, space_temp: use holiday-agnostic similar-weather weekday data
		"""

		is_holiday, _ = holidays_obj.is_holiday_dt(dt)
		dow = dt.isoweekday()

		match_found = False
		failover_forecast = []

		if self.options.debug:
			self.lgr.info('holiday_flag: %s, dow = %d' % (is_holiday, dow))

		# iterate sorted similar-weather-day list with closest weather day first
		for sim_dt, _ in similar_weather_days:

			is_holiday_tmp, _ = holidays_obj.is_holiday_dt(sim_dt)
			dow_tmp = sim_dt.isoweekday()

			if self.options.debug:
				self.lgr.info('sim dt: %s, holiday_flag: %s, dow = %d' % (
					sim_dt, is_holiday_tmp, dow_tmp))

			# non-holiday case: use most similar weather day with the same
			# day-of-week type for which data is available
			if not is_holiday:

				if not is_holiday_tmp and (self.day_of_week_type(dow) ==
				   self.day_of_week_type(dow_tmp)):

					match_found, failover_forecast = self.check_obs_avlblty(sim_dt,
						obs_obj)

			# if holiday, use data from a Saturday
			elif is_holiday:
				if self.day_of_week_type(dow_tmp) == 'SATURDAY':

					match_found, failover_forecast = self.check_obs_avlblty(
						sim_dt, obs_obj)

			if match_found:
				break

		if not len(failover_forecast):
			self.lgr.critical('Failed to find failover forecast')

		return failover_forecast



	def compute_failover_forecast(self, obs_obj,
						weather_obj, holidays_obj):
		""" find the most similar weather day with the actual observations
			available for hour and use the observations as the forecast
		"""

		f_labels = []

		if not self.keys or not len(self.keys):
			self.lgr.critical('No keys found')
			return f_labels

		# compute similar weather days
		weather_obj.compute_similar_weather_day_cache(self.keys,
			self.model_type)

		# find days with most similar weather
		dt = self.keys[0].date()
		similar_weather_days = weather_obj.similar_wetbulb_day_cache[dt]

		f_labels = self.find_best_failover(similar_weather_days, dt,
			obs_obj, holidays_obj)

		return f_labels



	def gen_failover_keys(self, hour, forecast_start_ts):
		""" generate failover keys
			related to: compile_covariates.gen_test_keys
		"""

		if forecast_start_ts is None:
			lgr.critical('forecast start ts must be set')
			return

		# start 30 minutes after run time to allow TPOCOM
		# time to send it to SIF/UI
		tmp_ts = forecast_start_ts + datetime.timedelta(minutes=30)

		gap_td = datetime.timedelta(minutes=self.options.forecast_granularity)
		end_ts = tmp_ts + datetime.timedelta(
			hours=self.options.forecast_length)

		keys = []
		while tmp_ts < end_ts:
			if tmp_ts.hour == hour:
				keys.append(tmp_ts)
			tmp_ts += gap_td

		self.lgr.info('failover keys: %s' % keys)
		return keys



	def check_tpo_alarm_status(self, cursr, model_type, floor_quad_info):
		""" check if tpo alarm already set """

		qry_curr_alarms = """
			SELECT ID, STATE, PROPERTY_PRIO, INTERNAL, INITTS, SIGN, SIGN_PROG
			FROM [%s].dbo.[%s]
			WHERE STATE > 0 AND NORMTS IS NULL AND PBS = 'TPO ALARM'
				AND sign_prog = '%s'
		""" % (self.options.results_db, self.options.alarms_table, self.sign_prog)

		try:
			cursr.execute(qry_curr_alarms)
		except Exception, e:
			self.lgr.critical('alarm read failed: %s' % traceback.format_exc())
			return False

		# check if alarm is already set
		for row in cursr.fetchall():
			id, state, priority, internal, start_ts, msg, prog = row
			
			if (model_type in msg and self.id in msg
				 and floor_quad_info in msg):

				self.lgr.info('existing alarm: state<%d>, priority<%d>, start_ts<%s>, msg<%s>, prog<%s>'
					% (state, priority, start_ts, msg, prog))

				if self.is_alarm_set(row, model_type, floor_quad_info, cursr):
					return True

		return False



	def set_tpo_alarm(self, failure_count, model_type,
			floor=None, quadrant=None):
		""" set tpo alarm for failover, if not already set """

		# connect
		cnxn, cursr = connect(self.options.db_driver,
			self.options.results_db_user, self.options.results_db_pwd,
			self.options.results_db, self.options.results_db_server)

		# floor/quadrant info
		floor_quad_info = ''
		if floor and quadrant:
			floor_quad_info = '(%s:%s)' % (floor, quadrant)

		if self.check_tpo_alarm_status(cursr, model_type,
			floor_quad_info):
			self.lgr.info('tpo alarm already set')
			cnxn.close()
			return
		
		# set the alarm
		self.lgr.info('setting tpo alarm now')

		# failure type
		failure_type = 'Total/partial'
		priority_code = 2 # yellow/amber
		# let us keep it steady amber for now
		# if failure_count == options.forecast_length:
			# failure_type = 'Total'
			# priority_code = 1 # red
		
		insert_stmt = """
			INSERT INTO [%s].dbo.[%s] (STATE, PROPERTY_PRIO, INTERNAL,
				INITTS, PBS, SIGN, SIGN_PROG)
			VALUES (3, %d, 0, ?, 'TPO ALARM',
				'%s forecast failure: %s %s %s', '%s')
		""" % (self.options.results_db, self.options.alarms_table,
			priority_code, failure_type, self.id,
			floor_quad_info, model_type, self.sign_prog)

		try:
			self.lgr.info(insert_stmt)
			cursr.execute(insert_stmt, self.run_ts)
			cnxn.commit()

		except Exception, e:
			self.lgr.critical('alarm set failed: %s' % traceback.format_exc())

		cnxn.close()


	def reset_alarm(self, alarm, cnxn, cursr, model_type, floor_quad_info):
		""" reset alarm:
			# 1. Change state to 0 of existing alarm
			2. Insert new row with alarm end time specified
		"""

		id, state, priority, internal, start_ts, msg, prog = alarm

		# set state field to 0 of the existing alarm
		# upd_stmt = """
			# UPDATE [%s].dbo.[%s]
			# SET STATE = 0
			# WHERE ID = %d""" % (self.options.results_db,
				# self.options.alarms_table, id)

		# cursr.execute(upd_stmt)
		
		# insert new row with alarm end time
		insert_stmt = """
			INSERT INTO [%s].dbo.[%s] (STATE, PROPERTY_PRIO, INTERNAL,
				INITTS, NORMTS, PBS, SIGN, SIGN_PROG)
			VALUES (0, ?, ?, ?, ?, 'TPO ALARM',
				'Forecast restored: %s %s %s', '%s')
		""" % (self.options.results_db, self.options.alarms_table,
			self.id, floor_quad_info, model_type, self.sign_prog)

		try:
			cursr.execute(insert_stmt, priority, internal, start_ts,
				self.run_ts)
		except Exception, e:
			self.lgr.critical('alarm reset failed <%s> : %s' % (
				alarm, traceback.format_exc()))



	def is_alarm_set(self, alarm, model_type, floor_quad_info, cursr):
		""" check if the selected alrm is currently set/active
		"""
		
		qry_reset_alarms = """
			SELECT ID, STATE, PROPERTY_PRIO, INTERNAL, INITTS, NORMTS, SIGN,
				SIGN_PROG
			FROM [%s].dbo.[%s]
			WHERE STATE = 0 AND INITTS = ? AND NORMTS IS NOT NULL
				AND PBS = 'TPO ALARM' AND SIGN_PROG = '%s'
		""" % (self.options.results_db, self.options.alarms_table,
			self.sign_prog)
		
		id, state, priority, internal, start_ts, msg, prog = alarm

		try:
			cursr.execute(qry_reset_alarms, start_ts)
		except Exception, e:
			self.lgr.critical('set alarm read failed: %s' % traceback.format_exc())
			return

		for row in cursr.fetchall():
			id, state, priority, internal, start_ts, end_ts, msg, prog = row
			
			if (model_type in msg and self.id in msg
				 and floor_quad_info in msg):
				self.lgr.info('alarm already reset <%s>' % row)
				return False

		return True


	def reset_tpo_alarm(self, model_type, floor=None, quadrant=None):
		""" reset any existing alarms for this
			<model-type, building, floor-quadrant> combination
		"""
		
		# floor/quadrant info
		floor_quad_info = ''
		if floor and quadrant:
			floor_quad_info = '(%s:%s)' % (floor, quadrant)

		# connect
		cnxn, cursr = connect(self.options.db_driver,
			self.options.results_db_user, self.options.results_db_pwd,
			self.options.results_db, self.options.results_db_server)

		qry_curr_alarms = """
			SELECT ID, STATE, PROPERTY_PRIO, INTERNAL, INITTS, SIGN, SIGN_PROG
			FROM [%s].dbo.[%s]
			WHERE STATE > 0 AND NORMTS IS NULL AND PBS = 'TPO ALARM'
				AND SIGN_PROG = '%s'
		""" % (self.options.results_db, self.options.alarms_table,
			self.sign_prog)

		try:
			cursr.execute(qry_curr_alarms)
		except Exception, e:
			self.lgr.critical('alarm read failed: %s' % traceback.format_exc())
			return

		# check if alarm(s) already set
		set_alarms = []
		for row in cursr.fetchall():
			id, state, priority, internal, start_ts, msg, prog = row

			if (model_type in msg and self.id in msg
				 and floor_quad_info in msg):

				self.lgr.info('alarm found: state<%d>, priority<%d>, start_ts<%s>, msg<%s>, prog<%s>'
					% (state, priority, start_ts, msg, prog))

				# check if this alarm has already been reset; forecasting modules
				# try to reset any related set alarm after each successful run
				is_set = self.is_alarm_set(row, model_type,
					floor_quad_info, cursr)
				
				if is_set:
					set_alarms.append(row)
		
		for alarm in set_alarms:
			self.reset_alarm(alarm, cnxn, cursr, model_type, floor_quad_info)

		cnxn.commit()
		cnxn.close()

