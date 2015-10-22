#!/bin/env python

""" generate failover VFD triggers
"""

__version__ = '$Id'
__author__ = 'ag2818@columbia.edu'
_module = 'vfd_trigger_failover'

import os
import sys
#from sets import Set
from collections import OrderedDict
import datetime
import math
import optparse
import cfgparse
import traceback
import numpy
import random

from common_rudin.common import log_from_config, setup, setup_cparser
import common_rudin.utils as utils
from common_rudin.db_utils import connect

from occupancy_lite import Occupancy_Lite
from common_rudin.holidays import Holidays

SKIP_HOLIDAYS = True
SKIP_WEEKENDS = True

# VFD trigger signal will be sent if a 2% or more move a observed from the most peak/valley
VFD_TRIGGER_THRESHOLD_PCT = 2.0 # in percent
MIN_TRIG_OCC = 30 # minimum inflection point occupancy for it to act as trigger

# constants
ONE_DAY = datetime.timedelta(hours=24)
THREE_DAYS = datetime.timedelta(days=3)

# minimum allowed separation between triggers of same type
MIN_SAME_TRIG_SEP = datetime.timedelta(hours=3)
MIN_DIFF_TRIG_SEP = datetime.timedelta(minutes=30)

def db_connect(options):
	return connect(options.db_driver, options.db_user,
		options.db_pwd, options.building_db,
		options.building_db_server)


def merge_obs(old_obs, new_obs, holiday_data, options, lgr):
	""" merge new_obs into old_obs
	"""

	# data format: occupancy
	for ts, val in new_obs.iteritems():
		if SKIP_WEEKENDS and ts.isoweekday() in [6, 7]:
			continue

		if SKIP_HOLIDAYS and ts.date() in holiday_data:
			continue

		ts_info = [val]

		# because of the continuing problem of mis-labelled occupancy
		# observations it is very likely to see an existing ts again with
		# an updated occupancy value
		if ts in old_obs:
			ts_info = old_obs[ts]
			ts_info[0] = val

		old_obs[ts] = ts_info
	
	return old_obs


triggs_query = """
	SELECT trigger_tm, vfd_action, run_ts FROM [%s].[dbo].%s
	WHERE trigger_tm > ?
	ORDER BY trigger_tm, run_ts
"""

def get_obs_triggers(vfd_triggers, options, lgr):
	""" get new triggers generated since the last trigger
		this should get <= 1 trigger most of the time unless the
		program failed / could-not-run over an extended period
	"""

	most_recent_trig_ts, most_recent_trig_type = get_recent_trigger(
		vfd_triggers, options, lgr)

	cnxn, cursr = connect(options.db_driver, options.results_db_user,
		options.results_db_pwd, options.results_db,
		options.results_db_server)

	query = triggs_query % (options.results_db,
		'occupancy_vfd_triggers_realtime')

	if options.debug is not None and options.debug == 1:
		lgr.info('executing %s' % query)

	cursr.execute(query, most_recent_trig_ts)
	
	new_triggers = OrderedDict([])
	for row in cursr.fetchall():
		trig_ts, trig_type, run_ts = row
		new_triggers[trig_ts] = trig_type

	cnxn.close()
	return new_triggers


def get_forecast_triggers(most_recent_trig_ts, options, lgr):
	""" get new triggers generated since the last trigger
		this should get <= 1 trigger most of the time unless the
		program failed / could-not-run over an extended period
	"""

	cnxn, cursr = connect(options.db_driver, options.results_db_user,
		options.results_db_pwd, options.results_db,
		options.results_db_server)

	query = triggs_query % (options.results_db,
		'occupancy_forecast_vfd_triggers')

	if options.debug is not None and options.debug == 1:
		lgr.info('executing %s' % query)

	cursr.execute(query, most_recent_trig_ts)
	
	new_triggers = OrderedDict([])
	for row in cursr.fetchall():
		trig_ts, trig_type, run_ts = row
		new_triggers[trig_ts] = trig_type

	cnxn.close()
	return new_triggers


def get_recent_triggers(run_ts, options, lgr):
	""" get the last few triggers realtime triggers
		this is used to help seed the program on the first run
	"""
	
	cnxn, cursr = connect(options.db_driver, options.results_db_user,
		options.results_db_pwd, options.results_db,
		options.results_db_server)

	query = triggs_query % (options.results_db,
		'occupancy_vfd_triggers_realtime')

	if options.debug is not None and options.debug == 1:
		lgr.info('executing %s' % query)

	ts = run_ts - datetime.timedelta(days=5)
	cursr.execute(query, ts)
	
	recent_triggers = OrderedDict([])
	for row in cursr.fetchall():
		trig_ts, trig_type, run_ts = row
		recent_triggers[trig_ts] = trig_type
	
	cnxn.close()
	return recent_triggers
	


insert_trigg = """
	INSERT INTO [%s].dbo.[%s] (trigger_tm, vfd_action, run_ts)
	VALUES (?, ?, ?)
"""

def save_triggers(triggers, run_ts, options, lgr):
	""" save new triggers to database """
	
	cnxn, cursr = connect(options.db_driver, options.results_db_user,
		options.results_db_pwd, options.results_db,
		options.results_db_server)
	
	insert_stmt = insert_trigg % (options.results_db,
		'occupancy_vfd_triggers')
	for trig_ts, trig_type in triggers.iteritems():
		cursr.execute(insert_stmt, trig_ts, trig_type, run_ts)

	cnxn.commit()
	cnxn.close()



def process_new_triggers(new_triggers, vfd_triggers, run_ts, modify_state,
		options, lgr):
	""" merge new triggers with existing trigger set and save new trigger(s)
		to database
	"""

	most_recent_trig_ts, most_recent_trig_type = get_recent_trigger(
		vfd_triggers, options, lgr)

	triggers_to_save = OrderedDict([])
	prev_trig_ts, prev_trig_type = most_recent_trig_ts, most_recent_trig_type
	for trig_ts, trig_type in new_triggers.iteritems():

		save_trig = True

		# if this and previous trigger are of the same type, make sure they
		# are separated in time
		if prev_trig_type and trig_type == prev_trig_type:
			if trig_ts - prev_trig_ts < MIN_SAME_TRIG_SEP:
				save_trig = False

		if save_trig:
			lgr.info('issuing trigger: %s : %s' % (trig_ts, trig_type))
			triggers_to_save[trig_ts] = trig_type
			vfd_triggers[trig_ts] = trig_type
		
		prev_trig_ts, prev_trig_type = trig_ts, trig_type

	if modify_state:
		save_triggers(triggers_to_save, run_ts, options, lgr)
	return vfd_triggers


def get_recent_trigger(vfd_triggers, options, lgr):
	""" get most recent trigger """
	
	trig_keys = vfd_triggers.keys()
	most_recent_trig_ts, most_recent_trig_type = None, None
	if len(trig_keys):
		most_recent_trig_ts = trig_keys[-1]
		most_recent_trig_type = vfd_triggers[most_recent_trig_ts]
	
	return [most_recent_trig_ts, most_recent_trig_type]


def process_failover_triggers(run_ts, vfd_triggers,
		modify_state, options, lgr):
	"""
	this is called only if the occupancy data is stale
	-> check if the forecast has a VFD trigger since the most recently
	issued trigger or the most recent obs ts, whichever is later
	"""

	most_recent_trig_ts, most_recent_trig_type = get_recent_trigger(
		vfd_triggers, options, lgr)
	
	lgr.info('most recent trigger ts: %s' % most_recent_trig_ts)

	forecast_triggs = get_forecast_triggers(most_recent_trig_ts, options, lgr)
	
	lgr.info('forecast triggs: %s' % str(forecast_triggs))

	triggers_to_save = OrderedDict([])
	prev_trig_ts, prev_trig_type = most_recent_trig_ts, most_recent_trig_type
	for trig_ts, trig_type in forecast_triggs.iteritems():
		
		# the fail-over trigger time must be after the most recent trigger but before
		# run time 
		if trig_ts > run_ts or trig_ts <= most_recent_trig_ts:
			continue
		
		# if this and previous trigger are of the same type, make sure they
		# are separated in time
		save_trig = True
		if prev_trig_type and trig_type == prev_trig_type:
			if trig_ts - prev_trig_ts < MIN_SAME_TRIG_SEP:
				save_trig = False
		
		else: # different types
			if trig_ts - prev_trig_ts < MIN_DIFF_TRIG_SEP:
				save_trig = False

		if save_trig:
			lgr.info('issuing failover trigger: %s : %s' %
				(trig_ts, trig_type))
			triggers_to_save[trig_ts] = trig_type
			vfd_triggers[trig_ts] = trig_type

		prev_trig_ts, prev_trig_type = trig_ts, trig_type
	
	if modify_state:
		save_triggers(triggers_to_save, run_ts, options, lgr)

	return vfd_triggers
	
	

STALE_OCCUPANCY_THRESH = datetime.timedelta(minutes=20)

def process_data(old_obs, new_obs, run_ts, modify_state, holiday_data,
		vfd_triggers, options, lgr):
	""" 
	"""

	# compute new keys
	keys = new_obs.keys()
	recent_ts = None
	if len(keys):
		recent_ts = keys[0]

	old_obs_len = len(old_obs)
	if old_obs_len:
		old_keys = old_obs.keys()
		prev_ts = old_keys[-1]
		
		# make sure prev_ts is not the same as recent_ts
		# this causes problems computing correct deltas and hence the triggers
		# for the mis-labelled observations
		if prev_ts == recent_ts:
			for idx in range(-2, -5, -1):
				if old_obs_len + idx >= 0:
					prev_ts = old_keys[idx]
					if prev_ts < recent_ts:
						break

		prev_occ = old_obs[prev_ts]
	
	# merge existing and new data for easier processing
	merged_obs = merge_obs(old_obs, new_obs, holiday_data, options, lgr)
	
	# find most recent timestamp
	newest_ts = None
	all_keys = merged_obs.keys()
	if len(all_keys):
		newest_ts = all_keys[-1]
	
	# -> if occupancy data is > 30 minutes old and a trigger is forecasted,
	# send forecasted trigger and record the replacement
	# -> any new trigger of the same type generated with a  [+-]1 hour range of
	# the forecasted trigger will be suppressed for suspicion of being a duplicate
	# -> the [+-] is required because it is not uncommon for occupancy data to arrive
	# in a burst with old data coming in as well which may cause a duplicate trigger
	
	# ag2818: there may be failover triggers that need to be generateds
	#if not newest_ts:
	#	return [merged_obs, vfd_triggers]

	if newest_ts:
		newest_dt = newest_ts.date()
		lgr.info('newest obs: %s' % newest_ts)

	if newest_ts is None or run_ts - newest_ts > STALE_OCCUPANCY_THRESH:
		lgr.info('run_ts: %s, newest_ts: %s' % (run_ts, newest_ts))
		vfd_triggers = process_failover_triggers(run_ts, vfd_triggers,
			modify_state, options, lgr)

	else:
		# check if new triggers has been created that need to be copied over
		new_triggers = get_obs_triggers(vfd_triggers, options, lgr)

		trigg_count = len(new_triggers)
		lgr.info('%d new trigger(s) found' % trigg_count)
		if trigg_count:
			vfd_triggers = process_new_triggers(new_triggers, vfd_triggers,
				run_ts, modify_state, options, lgr)

	return [merged_obs, vfd_triggers]



def reload_state(building_id, options ,lgr):
	""" reload last state from disk """

	obs = OrderedDict([])
	obs = utils.unpickler('%s_occupancy_data_failover.p' % building_id, obs,
		lgr, options)

	vfd_triggers = OrderedDict([])
	vfd_triggers = utils.unpickler('%s_vfd_triggers.p' % building_id,
		vfd_triggers, lgr, options)

	# reload holidays data
	holiday_data = {}
	holiday_data = utils.unpickler('%s_holiday_data_failover.p' % building_id,
		holiday_data, lgr, options)

	return [obs, vfd_triggers, holiday_data]



def trim_data(obs, vfd_triggers, as_of_ts):
	""" discard old data to keep saved state footprint small """

	# trim occupancy data
	trimmed_obs = OrderedDict([])
	for ts, val in obs.iteritems():
		if as_of_ts - ts < 5*ONE_DAY:
			trimmed_obs[ts] = val

	trimmed_triggers = OrderedDict([])
	for ts, val in vfd_triggers.iteritems():
		if as_of_ts - ts < 5*ONE_DAY:
			trimmed_triggers[ts] = val

	return [trimmed_obs, trimmed_triggers]



def save_state(obs, vfd_triggers, holiday_data, as_of_ts, building_id,
		options, lgr):
	""" save state to disk """

	lgr.info('before trim: %s' % vfd_triggers)
	obs_trim, vfd_triggers_trim = trim_data(obs, vfd_triggers,
		as_of_ts)

	lgr.info('trimmed triggs: %s' % vfd_triggers_trim)
	utils.pickler('%s_occupancy_data_failover.p' % building_id, obs_trim, lgr,
		options)
	utils.pickler('%s_vfd_triggers.p' % building_id, vfd_triggers_trim, lgr,
		options)
	utils.pickler('%s_holiday_data_failover.p' % building_id, holiday_data,
		lgr, options)



def refresh_holidays(holiday_data, run_ts, options, lgr):
	""" decide if holiday data needs to be refreshed """
	
	# this is an optimization to avoid re-leoading holiday data on every run
	# refresh holiday data only if it there is no data available in the loaded state
	# or if run hour is an even number and the random number is <= 0.1
	# the holiday will be refreshed during even hour runs about every 1 in 10 runs
	if len(holiday_data):
		if random.random() > 0.1 or run_ts.hour%2:
			return holiday_data

	# re-load holidays
	lgr.info('refreshing holiday data')
	holidays_obj = Holidays(options, lgr)
	if options.debug:
		lgr.info('holidays : %s' % holidays_obj.holidays)
	return holidays_obj.holidays



def main(argv):
	""" driver function """

	if argv is None:
		argv = sys.argv

	version = "%prog 0.1"
	usage = "usage: %prog [options]"

	oparser = optparse.OptionParser(usage=usage, version=version,
		description=__doc__)
	cparser = cfgparse.ConfigParser()
	setup(oparser, cparser, _module)

	options, args = cparser.parse(oparser, argv)

	lgr = log_from_config(options, _module)
	lgr.info('*** %s starting up' % _module)
	
	arg_count = len(args)

	run_ts = datetime.datetime.now()
	lgr.info('run time: %s' % run_ts)

	load_prev_state = True
	# user-specified run_ts?
	if arg_count == 1:
		as_of_ts = run_ts
		
	else:
		lgr.critical(args)
		oparser.error("incorrect number of arguments")

	# whether to modiy existing saved state and save data to database
	# existing state is not modified in a debug run and when the program
	#   is as of a date in the past
	lgr.info('debug: %s, load_prev_state: %s' % (options.debug, load_prev_state))
	modify_state = False
	if load_prev_state and not options.debug:
		modify_state = True
	else:
		lgr.info('running in read-only mode')

	# get building ids
	building_ids = utils.parse_value_list(options.building_ids)

	reinstantiate_cparser = False
	for bldg_idx, building_id in enumerate(building_ids):

		lgr.info('processing building %s' % building_id)
		if '345' not in building_id:
			lgr.info('skipping building')
			continue

		try:

			if bldg_idx != 0:
				reinstantiate_cparser = True
			options = utils.load_bldg_config(building_id, oparser, cparser, argv,
				options, lgr, reinstantiate_cparser)

			saved_obs_data = OrderedDict([])
			holiday_data = {}

			# load occupancy state data from last run
			last_obs_ts = None
			if modify_state:
				lgr.info('loading saved state')
				prev_state = reload_state(building_id, options, lgr)
				saved_obs_data, vfd_triggers, holiday_data = prev_state

				keys = saved_obs_data.keys()
				if len(keys):
					last_obs_ts  = keys[-1]
			else:
				lgr.warn('skipped loading previous state')
			
			if not last_obs_ts:
				last_obs_ts = as_of_ts - datetime.timedelta(hours=12)
			lgr.info('last obs ts: %s' % last_obs_ts)

			# refresh holiday data
			holiday_data = refresh_holidays(holiday_data, run_ts, options, lgr)
			
			# read recent occupancy data
			occ_obj = Occupancy_Lite(lgr, options, last_obs_ts, building_id)
			
			# if no previous VFD triggers, load the last few triggers
			if not len(vfd_triggers):
				vfd_triggers = get_recent_triggers(run_ts, options, lgr)
				lgr.info('seed vfd triggers: %s' % vfd_triggers)
			else:
				lgr.info('re-loaded vfd triggers: %s' % vfd_triggers)

			obs, vfd_triggers = process_data(saved_obs_data, occ_obj.data, run_ts,
				modify_state, holiday_data, vfd_triggers, options, lgr)
			lgr.info('updated vfd triggers: %s' % vfd_triggers)

			# save occupancy state data for next run
			if modify_state:
				lgr.info('saving state')
				save_state(obs, vfd_triggers, holiday_data, as_of_ts,
					building_id, options, lgr)
			else:
				lgr.info('state was not saved')
		
		except Exception, e:
			lgr.info('Failed for building %s: %s' % (building_id,
				traceback.format_exc()))


if __name__ == '__main__':
	main(sys.argv)
