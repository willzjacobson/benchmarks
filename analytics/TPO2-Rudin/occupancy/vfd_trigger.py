#!/bin/env python

""" predict occupancy of the building based on
	past observations and other covariates
"""

__version__ = '$Id'
__author__ = 'ag2818@columbia.edu'
_module = 'vfd_trigger'

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
#from common_rudin.weather import Weather
from common_rudin.holidays import Holidays

SKIP_HOLIDAYS = True
SKIP_WEEKENDS = True

# VFD trigger signal will be sent if a 2% or more move a observed from the most peak/valley
VFD_TRIGGER_THRESHOLD_PCT = 2.0 # in percent
MIN_TRIG_OCC = 30 # minimum inflection point occupancy for it to act as trigger

# constants
ONE_DAY = datetime.timedelta(hours=24)
THREE_DAYS = datetime.timedelta(days=3)

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='valid')
    return y


def compute_moving_average(old_obs, new_obs):
	""" compute moving average data """
	
	WINDOW_SZ = 3

	keys = old_obs.keys()
	tmp_obs = OrderedDict([])

	# get WINDOW - 1 obs from old data
	if len(old_obs) >= WINDOW_SZ - 1:
		old_keys = old_obs.keys()
		for idx in range(-1*WINDOW_SZ + 1, -1):
			ts = old_keys[idx]
			tmp_obs[ts], _, _, _, _, _ = old_obs[ts]
		
	for ts, occ in new_obs.iteritems():
		tmp_obs[ts] = occ
	
	print len(tmp_obs.values())
	tmp_obs_smooth = smooth(numpy.asarray(tmp_obs.values()), window_len=WINDOW_SZ,
		window='flat')
	print len(tmp_obs_smooth)

	new_obs_smooth = OrderedDict([])
	for idx, ts in enumerate(new_obs.keys()):
		new_obs_smooth[ts] = tmp_obs_smooth[idx]
	return new_obs_smooth


def db_connect(options):
	return connect(options.db_driver, options.db_user,
		options.db_pwd, options.building_db,
		options.building_db_server)


def save_trigger(ts, trig_type, run_ts, options, lgr):
	""" save VFD trigger to DB """
	
	insert_stmt = """
		INSERT INTO [%s].dbo.[%s]
		(trigger_tm, vfd_action, run_ts)
		VALUES (?, ?, ?)
	""" % (options.results_db, 'occupancy_vfd_triggers')#options.occ_vfd_trigger_table) TODO

	cnxn, cursr = db_connect(options)
	cursr.execute(insert_stmt, ts, trig_type, run_ts)
	cnxn.commit()
	cnxn.close()
	

def save_deltas(keys, obs, run_ts, options, lgr):
	""" save VFD trigger to DB """
	
	if not len(keys):
		lgr.info('nothing to save')
		return

	insert_stmt = """
		INSERT INTO [%s].dbo.[%s]
		(run_ts, occupancy_ts, delta)
		VALUES (?, ?, ?)
	""" % (options.results_db, 'occupancy_vfd_trigger_deltas')#options.occ_vfd_trigger_table) TODO

	cnxn, cursr = db_connect(options)

	insert_seq = []
	for ts in keys:
		# weekends/holidays may have been removed
		if SKIP_HOLIDAYS or SKIP_WEEKENDS:
			if ts not in obs:
				continue
		insert_seq.append((run_ts, ts, obs[ts][2]))

	cursr.executemany(insert_stmt, insert_seq)
	cnxn.commit()
	cnxn.close()


def merge_obs(old_obs, new_obs, holiday_data, options, lgr):
	""" merge new_obs into old_obs
	"""
	#moving_avgs = compute_moving_average(old_obs, new_obs)

	# data format: occupancy, smooth_occ, delta, inflection_pt_flg, triggered ramp-down/ramp-up, trigger type
	for ts, val in new_obs.iteritems():
		if SKIP_WEEKENDS and ts.isoweekday() in [6, 7]:
			continue

		if SKIP_HOLIDAYS and ts.date() in holiday_data:
			continue

		ts_info = [val, None, None, None, False, None]
		# because of the continuing problem of mis-labelled occupancy
		# observations it is very likely to see an existing ts again with
		# an updated occupancy value
		if ts in old_obs:
			ts_info = old_obs[ts]
			ts_info[0] = val

		old_obs[ts] = ts_info

	if options.debug:
		utils.write_dict_to_csv(old_obs, '%s_merged_obs.csv' % options.building_id, None)
	
	return old_obs


# maximum allowed gap for determining a valid trend reversal
MAX_GAP_TREND_RVRSL = datetime.timedelta(hours=3)

def is_trend_reversal(delta, prev_ts, prev_delta, obs):
	""" check if there is a trend reversal separated by one of more
		constant observations
		
	"""
	
	keys = obs.keys()
	
	for ts in reversed(keys):
		if ts >= prev_ts:
			continue
		
		if prev_ts - ts > MAX_GAP_TREND_RVRSL:
			break
		occ, _, delta_tmp, inf_flag, trig, _ = obs[ts]

		if delta_tmp:
			if (delta_tmp > 0 and delta < 0) or (delta_tmp < 0 and delta > 0):
				return True
			break
	
	return False


CLEAR_INFL_THRESHOLD = 5

def is_clear_inflection(ts, delta, prev_ts, prev_delta, obs):
	""" is clear/convincing inflection """
	if (abs(delta) < CLEAR_INFL_THRESHOLD
		or abs(prev_delta) < CLEAR_INFL_THRESHOLD):

			return False
	
	return True
	
	

def is_inflection_pt(ts, delta, occ, prev_ts, prev_delta, prev_occ, obs):
	""" check if ts is an inflection point
		at an inflection point, the derivative changes sign
	"""

		# general condition
		# must be clear/convincing inflection point
	if ((delta and prev_delta and ((prev_delta < 0 and delta > 0)
			or (prev_delta > 0 and delta < 0)))
			#and is_clear_inflection(ts, delta, prev_ts, prev_delta, obs))

		# morning arrivals
		or (not prev_occ and delta) # or (prev_delta and not delta)

		# trend reversal separated by a string of constant values
		or (not prev_delta and delta and is_trend_reversal(delta, prev_ts, prev_delta, obs))):

			# prev_ts and ts are more than an hour apart, don't trust them
			if ts - prev_ts < datetime.timedelta(hours=1):
				return True
		
	return False


def get_last_trigger_type(inflection_pts, trigger_pts, obs):
	""" get trigger type for the most recent trigger """
	
	for idx, inflection_pt in enumerate(reversed(inflection_pts)):
		occ, occ_smth, delta, inf_flag, trig, trig_type = obs[inflection_pt]
		if trig:
			trig_ts = None
			if len(trigger_pts) >= idx + 1:
				trig_ts = trigger_pts[-1 * (idx + 1)]
			return [inflection_pt, trig_type, trig_ts]

	return [None, None, None]


def get_last_trigger_type_new(trigger_pts, obs=None):
	""" get trigger type for the most recent trigger """
	
	keys = trigger_pts.keys()
	if len(keys):
		last_trig_ts = keys[-1]
		trig_info = trigger_pts[last_trig_ts]
		return [trig_info['infl_ts'], trig_info['trig_type'], last_trig_ts]

	return [None, None, None]


EIGHTEEN_HOURS = datetime.timedelta(hours=18)
THIRTY_MINUTES = datetime.timedelta(minutes=30)


def is_vfd_trigger(ts, occ, inflection_pts, trigger_pts, obs, max_occ,
		options, lgr):
	""" is the curent occupancy a trigger for VFDs?
	VFDs rapdown/rampdown needs to be triggered when occupancy increases by
	threshold % from a bottom or drops threshold % from a peak
	"""

	# if no inflection points have been found, there is nothing to do
	if not len(inflection_pts):
		return [False, None, None]

	occ_dt = ts.date()

	# get most recent trigger sent and its type
	trig_infl_ts, last_trig_type, last_trig_ts = get_last_trigger_type_new(
		trigger_pts, obs)
	last_trig_dt = None
	if last_trig_ts:
		last_trig_dt = last_trig_ts.date()

	for inflection_pt in reversed(inflection_pts):

		#last_inflection_pt = inflection_pts[-1]
		infl_occ, infl_occ_smth, inf_delta, inf_flag, inf_trig, trig_type_inf = obs[inflection_pt]
		#if trig_type_inf and trig_type_inf != last_trig_type:
		#if prev_delta and (prev_delta < 0 and delta > 0) or (prev_delta > 0 and delta < 0):

		# if we get to a inflection which has already caused a trigger, stop looking
		# do not trigger from inflection points from past days
		if inf_trig or ts - inflection_pt > ONE_DAY or ts.date() != inflection_pt.date():
			break

		#delta = abs(occ - infl_occ)
		#trigger_delta = VFD_TRIGGER_THRESHOLD_PCT*infl_occ/100.0
		delta = abs(occ - infl_occ)
		trigger_delta = VFD_TRIGGER_THRESHOLD_PCT*max(infl_occ, max_occ['occ'])/100.0
		if (not inf_trig and occ >= MIN_TRIG_OCC and delta >= trigger_delta):

			trig_type = 0
			if occ > infl_occ:
				trig_type = 1

			# 	no known previous trigger
			if (not last_trig_ts or
				# last trigger was more than threshold interval ago
				(last_trig_type == trig_type and ts - last_trig_ts > EIGHTEEN_HOURS) or #last_trig_dt != occ_dt or
				# last known trigger occured today and was of different type
				# and was at least thresold interval ago
				#(occ_dt == inflection_pt.date() and last_trig_type != trig_type
				#(occ_dt == last_trig_dt and last_trig_type != trig_type
				(last_trig_type != trig_type and ts - last_trig_ts > THIRTY_MINUTES)):

					print 'trigger: infl pt = %s, trigger obs = %s, last_trig_ts = %s, ts = %s' % (inflection_pt, occ, last_trig_ts, ts)
					print 'max occ: %s' % max(infl_occ, max_occ['occ'])
					obs[inflection_pt] = [infl_occ, infl_occ_smth, delta, inf_flag, True, trig_type]
					return [True, trig_type, inflection_pt]
			#else:
			#	print 'skipping trigger %s: %s' % (ts, inflection_pt)

	return [False, None, None]



def is_startup_trigger(ts, trig_type, trigger_pts, options, lgr):
	""" determine if is this trigger for morning startup """

	# UPDATE 2: save start-up trigger
	return False

	if trig_type == 0:
		return False

	trigger_tss = trigger_pts.keys()
	ts_dt = ts.date()
	
	prev_trig_ts = None
	for trig_ts in trigger_tss:
	
		if trig_ts == ts:

			if prev_trig_ts:
				if prev_trig_ts.date() != ts_dt and trig_type == 1:
					return True
			
			else:
				if ts.hour < 12 and trig_type == 1:
					return True

		prev_trig_ts = trig_ts

	return False


def process_data(old_obs, new_obs, inflection_pts, trigger_pts, run_ts,
		modify_state, max_occ, holiday_data, options, lgr):
	""" compute delta for new data and update inflection pt if a new one
		is present in the new data
	"""

	prev_occ, prev_delta, prev_ts, inflection_pt = None, None, None, []

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

		prev_occ, prev_occ_smth, prev_delta, _, _, _ = old_obs[prev_ts]
	
	# merge existing and new data for easier processing
	merged_obs = merge_obs(old_obs, new_obs, holiday_data, options, lgr)

	for ts in keys:
	
		# weekends/holidays may have been removed
		if SKIP_HOLIDAYS or SKIP_WEEKENDS:
			if ts not in merged_obs:
				continue
		
		occ, occ_smth, _, _, _, _ = merged_obs[ts]
		# update max occupancy
		if ts - max_occ['ts'] > 5*ONE_DAY or max_occ['occ'] < occ:
			max_occ['occ'] = occ
			max_occ['ts'] = ts

		delta = None		
		if prev_occ is not None:
			delta = occ - prev_occ
			
		ts_info = [occ, occ_smth, delta, False, False, None]

		# is inflection point?
		if prev_ts not in inflection_pts:
			if is_inflection_pt(ts, delta, occ, prev_ts, prev_delta,
					prev_occ, merged_obs):

				if options.debug:
					lgr.info('inflection pt: %s <%s>' % (prev_ts, prev_delta))
				inflection_pts.append(prev_ts)
				
				# this must index the is_inflection_pt flag
				# we find out about an inflection point when we are at its
				# immediately following point
				merged_obs[prev_ts][-3] = True

		# if occ is threshold pct off a high or threshold pct. over the most recent low
		if ts not in trigger_pts:
			is_trigger, trig_type, infl_pt_ts = is_vfd_trigger(ts, occ, inflection_pts,
				trigger_pts, merged_obs, max_occ, options, lgr)
			if is_trigger:
				trigger_pts[ts] = {'infl_ts': infl_pt_ts, 'trig_type' : trig_type}
				
				# UPDATE: Do not save start-up trigger, but keep it as part
				# of the internal state to avoid breaking the algorithm
				if not is_startup_trigger(ts, trig_type, trigger_pts, options, lgr):

					lgr.info('triggering vfds to %s at %s' % (trig_type, ts))
					if modify_state:
						save_trigger(ts, trig_type, run_ts, options, lgr)

				else:
					lgr.info('skipping startup trigger at %s' % ts)

		merged_obs[ts] = ts_info

		# save for next iteration
		prev_delta = delta
		prev_occ = occ
		prev_ts = ts
	
	for ts, info in merged_obs.iteritems():
		occ, occ_smth, delta, inf_pt, trig, trig_type = info
		if inf_pt or trig:
			lgr.info('%s: %s' % (ts, info))
	
	return [merged_obs, inflection_pts, trigger_pts, max_occ]



def reload_state(building_id, options ,lgr):
	""" reload last state from disk """

	obs = OrderedDict([])
	obs = utils.unpickler('%s_occupancy_data.p' % building_id, obs,
		lgr, options)
	
	infl_pts = []
	infl_pts = utils.unpickler('%s_inflection_pts.p' % building_id,
		infl_pts, lgr, options)
	
	if options.debug:
		lgr.info('inflection points: %s' % infl_pts)
	
	trigger_pts = OrderedDict([])
	trigger_pts = utils.unpickler('%s_trigger_pts.p' % building_id,
		trigger_pts, lgr, options)
	
	if options.debug:
		lgr.info('trigger points: %s' % trigger_pts)
	
	max_occ = {'ts': datetime.datetime.min, 'occ': -sys.maxint - 1}
	max_occ = utils.unpickler('%s_max_occ.p' % building_id,
		max_occ, lgr, options)
	if options.debug:
		lgr.info('max occ: %s' % max_occ)

	# reload holidays data
	holiday_data = {}
	holiday_data = utils.unpickler('%s_holiday_data.p' % building_id,
		holiday_data, lgr, options)
	
	return [obs, infl_pts, trigger_pts, max_occ, holiday_data]


def trim_data(obs, inflection_pts, trigger_pts, as_of_ts):
	""" discard old data to keep saved state footprint small """

	# trim occupancy data
	trimmed_obs = OrderedDict([])
	for ts, val in obs.iteritems():
		if as_of_ts - ts < ONE_DAY:
			trimmed_obs[ts] = val

	# trim inflection point data
	trimmed_infl_pts = []
	for ts in inflection_pts:
		if as_of_ts - ts < ONE_DAY:
			trimmed_infl_pts.append(ts)

	trimmed_trigger_pts = OrderedDict([])
	for ts, info in trigger_pts.iteritems():
		if as_of_ts - ts < ONE_DAY:
			trimmed_trigger_pts[ts] = info

	return [trimmed_obs, trimmed_infl_pts, trimmed_trigger_pts]


def save_state(obs, inflection_pts, trigger_pts, max_occ, holiday_data,
		as_of_ts, building_id, options, lgr):
	""" save state to disk """

	obs_trim, infl_pts_trim, trig_pts_trim = trim_data(obs, inflection_pts,
		trigger_pts, as_of_ts)

	utils.pickler('%s_occupancy_data.p' % building_id, obs_trim, lgr, options)
	utils.pickler('%s_inflection_pts.p' % building_id, infl_pts_trim,
		lgr, options)
	utils.pickler('%s_trigger_pts.p' % building_id, trig_pts_trim,
		lgr, options)
	utils.pickler('%s_max_occ.p' % building_id, max_occ,
		lgr, options)
	utils.pickler('%s_holiday_data.p' % building_id, holiday_data,
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

	elif arg_count == 6:
		int_args = map(int, args[1:])
		as_of_ts = datetime.datetime(int_args[0], int_args[1], int_args[2],
			int_args[3], int_args[4])
		load_prev_state = False
		
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
			
			inflection_pts, trigger_pts = [], OrderedDict([])
			# maximum occupancy and the time it was observed
			# this data structure keeps track of the maximum occupancy
			# observed in the past 24 hours
			max_occ = {'occ': -sys.maxint - 1, 'ts': datetime.datetime.min}
			saved_obs_data = OrderedDict([])
			holiday_data = {}

			# load occupancy state data from last run
			last_obs_ts = None
			if modify_state:
				lgr.info('loading saved state')
				prev_state = reload_state(building_id, options, lgr)
				saved_obs_data, inflection_pts, trigger_pts, max_occ, holiday_data = prev_state

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

			obs, inflection_pts, trigger_pts, max_occ = process_data(
				saved_obs_data, occ_obj.data, inflection_pts, trigger_pts,
				run_ts, modify_state, max_occ, holiday_data, options, lgr)

			# save occupancy state data for next run
			if modify_state:
				lgr.info('saving deltas and state')
				save_deltas(occ_obj.data.keys(), obs, run_ts, options, lgr)
				save_state(obs, inflection_pts, trigger_pts, max_occ,
					holiday_data, as_of_ts, building_id, options, lgr)
			else:
				lgr.info('deltas and state were not saved')
		
		except Exception, e:
			lgr.info('Failed for building %s: %s' % (building_id,
				traceback.format_exc()))


if __name__ == '__main__':
	main(sys.argv)
