#!/bin/env python

__version__ = '$Id'
__author__ = 'ag2818@columbia.edu'
_module = 'vfd_scenario_gen'

__doc__ = """ genrate scenarios for VFD data
		  """

import sys
from collections import OrderedDict
import math
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
from pylab import *

import optparse
import cfgparse
import traceback
from common_rudin.common import log_from_config, setup, setup_cparser

sample_vfd_data = []
sample_vfd_data_dict = {
	dt.datetime(2015, 1, 30, 0, 0, 0, 0) : [0, 0], 
	dt.datetime(2015, 1, 30, 0, 15, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 0, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 0, 45, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 1, 0, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 1, 15, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 1, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 1, 45, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 2, 0, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 2, 15, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 2, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 2, 45, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 3, 0, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 3, 15, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 3, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 3, 45, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 4, 0, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 4, 15, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 4, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 4, 45, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 5, 0, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 5, 15, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 5, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 5, 45, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 6, 0, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 6, 15, 0, 0) : [41.5, 41.5],
	dt.datetime(2015, 1, 30, 6, 30, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 6, 45, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 7, 0, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 7, 15, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 7, 30, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 7, 45, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 8, 0, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 8, 15, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 8, 30, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 8, 45, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 9, 0, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 9, 15, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 9, 30, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 9, 45, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 10, 0, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 10, 15, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 10, 30, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 10, 45, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 11, 0, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 11, 15, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 11, 30, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 11, 45, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 12, 0, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 12, 15, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 12, 45, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 13, 0, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 13, 15, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 13, 30, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 13, 45, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 14, 0, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 14, 15, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 14, 30, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 14, 45, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 15, 0, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 15, 15, 0, 0) : [49.4, 49.4],
	dt.datetime(2015, 1, 30, 15, 30, 0, 0) : [49.3, 49.3],
	dt.datetime(2015, 1, 30, 15, 45, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 16, 0, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 16, 15, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 16, 30, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 16, 45, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 17, 0, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 17, 15, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 17, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 17, 45, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 18, 0, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 18, 15, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 18, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 18, 45, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 19, 0, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 19, 15, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 19, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 19, 45, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 20, 0, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 20, 15, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 20, 30, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 20, 45, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 21, 0, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 21, 15, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 21, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 21, 45, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 22, 0, 0, 0) : [50.6, 50.6],
	dt.datetime(2015, 1, 30, 22, 15, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 22, 30, 0, 0) : [0, 0],
	dt.datetime(2015, 1, 30, 22, 45, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 23, 0, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 23, 15, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 23, 30, 0, 0) : [50.5, 50.5],
	dt.datetime(2015, 1, 30, 23, 45, 0, 0) : [50.5, 50.5],
}

class ScenarioGen:
	""" generate scenarios for VFD data """
	
	change_pts = []
	vfd_scheds = None
	THRESHOLD_CHANGE = 5 # in RPMs
	
	LEFT, RIGHT, DOWN = 'Left', 'Right', 'Down'
	MOVES = [LEFT, RIGHT, DOWN]
	
	def __init__(self, vfd_data):
		self.vfd_scheds = vfd_data
		self.change_pts = self.find_change_points_df(self.vfd_scheds)
		print self.change_pts


	def find_change_points(self, vfd_scheds):
		""" find change points
			change points are any change >= THRESHOLD_CHANGE
		"""
		# stores changes points for all VFDs in order
		change_pts_all = []
		
		for i, vfd_sched in enumerate(vfd_scheds):
		
			# stores changes pints for this VFD
			vfd_change_pts = []
			prev_ts, prev_freq = None, None
			
			# iterate over each frequency value for the VFD 
			for j, data in enumerate(vfd_sched.iteritems()):
				ts, freq = data
				
				# check for large move
				if prev_freq and abs(prev_freq - freq) >= self.THRESHOLD_CHANGE:
					vfd_change_pts.append(j)
				
				prev_ts, prev_freq = ts, freq
					
			change_pts_all.append(vfd_change_pts)
		
		return change_pts_all
	
	
	def find_change_points_df(self, vfd_df):
		""" find change points
			change points are any change >= THRESHOLD_CHANGE
		"""
		# stores changes points for all VFDs in order
		change_pts_all = [[] for i in range(vfd_df.shape[1])]

		prev_idx, prev_row = None, None

		for idx, sched_row in vfd_df.iterrows():

			# check for large moves
			if prev_row is not None:
				changed_vfds = np.flatnonzero(
					abs(prev_row - sched_row) >= self.THRESHOLD_CHANGE)

				for vfd in changed_vfds:
					change_pts_all[vfd].append(idx)
				
			prev_row, prev_idx = sched_row, idx
		
		return change_pts_all


	def select_change_point(self, change_pt_id, vfd_id_list):
		""" select change point """

		if change_pt_id:
			return change_pt_id

		# no change point specified
		# find change point counts of the short-listed vfds
		vfd_chg_pt_length = []
		for vfd_id in vfd_id_list:
			vfd_chg_pt_length.append(len(self.change_pts[vfd_id]))
		
		print ' vfd chg pt lengths: %s' % vfd_chg_pt_length

		# find shortest change point list length
		min_chg_pt_list_len = min(vfd_chg_pt_length)
		print 'min_chg_pt_list_len: %s' % min_chg_pt_list_len
		
		# pick a random change point id from this list,
		# each id being equally likely to be picked
		return np.random.randint(0, min_chg_pt_list_len)


	def _custom_round(self, x):
		"""round float to closest int"""
		int_x = int(math.floor(x))
		#if x - 0.5 >= int_x:
		#	return int_x + 1
		return int_x if x - 0.5 < int_x else int_x + 1


	def dt64_to_dt(self, dt64_data):
		""" convert numpy dt64 to datetime list """

		if isinstance(dt64_data, list):
			dt = []
			for t_dt64 in dt64_data:
				dt.append(pd.to_datetime(str(t_dt64)).replace(tzinfo=None))
			return dt

		else:
			return pd.to_datetime(str(dt64_data)).replace(tzinfo=None)


	def _shift_sanity_check(self, chg_pt, vfd_ids, shift_type, shift_mag,
			options, lgr):
		""" sanity check; make sure the shift maginude does not
			coincide/cross the next change point for all short-listed VFDs
		"""

		# list of timestamps in the dataframe
		idx_list = self.dt64_to_dt(list(self.vfd_scheds.index.values))

		for vfd_id in vfd_ids:
			chg_pt_list = self.change_pts[vfd_id]
			
			chg_pt_ts = chg_pt_list[chg_pt]
			chg_pt_idx = idx_list.index(chg_pt_ts)

			print self.vfd_scheds.idxmin(0).at[vfd_id]
			print 'chg pt: %s' % chg_pt
			print 'vfd id: %s' % vfd_id
			print 'freq: %s' % self.vfd_scheds.at[chg_pt_ts, vfd_id]
			
			# if corner change point
			if (shift_type in [self.LEFT, self.RIGHT]
			   and chg_pt in [0, len(chg_pt_list) - 1]):

				print 'corner chg pt case'
				if shift_type == self.LEFT:
					delta = chg_pt_ts - self.vfd_scheds.idxmin(0).at[vfd_id]
					print ' delta %s' % delta
					if shift_mag > delta:
						raise Exception('corner shift magnitude too large')

				elif shift_type == self.RIGHT:
					delta =  self.vfd_scheds.idxmax(0).at[vfd_id] - chg_pt_ts
					print ' delta %s' % delta
					if shift_mag > delta:
						raise Exception('corner shift magnitude too large')

				else:
					raise Exception('unsupported shift type')
			
			else:
				# reject shift if shift magnitude collides/goes beyond closest
				# change point in the direction
				# for down shifts, reduce rpm by threshold
				if shift_type == self.LEFT:
					delta = chg_pt_ts - chg_pt_list[chg_pt - 1]
					print 'delta %s' % delta
					if shift_mag >= delta:
						raise Exception('shift magnitude too large')

				elif shift_type == self.RIGHT:
					delta =  chg_pt_list[chg_pt + 1] - chg_pt_ts
					print 'delta %s' % delta
					if shift_mag >= delta:
						raise Exception('shift magnitude too large')

				elif shift_type == self.DOWN:
					# find freq immediately to the left and right of the chg pt 
					left_freq, rt_freq = None, None
					if chg_pt_idx > 0:
						left_freq = self.vfd_scheds.iat[chg_pt_idx-1, vfd_id]
					if chg_pt_idx < len(idx_list) - 1:
						rt_freq = self.vfd_scheds.iat[chg_pt_idx+1, vfd_id]

					
					# Recall: change is the first point of the new freq level
					chg_pt_freq = self.vfd_scheds.iat[chg_pt_idx, vfd_id]
					if left_freq and left_freq > chg_pt_freq:
						print 'chg pt freq: left'
						chg_pt_freq = left_freq

					elif rt_freq and rt_freq > chg_pt_freq:
						print 'chg pt freq: rt'
						chg_pt_freq = rt_freq

					print 'chg pt freq: %s' % chg_pt_freq
					if chg_pt_freq < self.THRESHOLD_CHANGE:
						raise Exception('shift magnitude too large')

				else:
					raise Exception('unsupported shift type')
	

	#def cpy_data(self, vfd_id, start_idx, end_idx, df):
	
	def execute_shift(self, shift_mag, shift_type, chg_pt, vfd_ids,
			options, lgr):
		""" shift VFD schedules """
		
		shifted_vfd_df = self.vfd_scheds.copy(True)
		idx_list = self.dt64_to_dt(list(shifted_vfd_df.index.values))
		print 'shift mag : ' + str(shift_mag)
		
		for vfd_id in vfd_ids:
			
			chg_pt_list = self.change_pts[vfd_id]
			chg_pt_ts = chg_pt_list[chg_pt]
			chg_pt_idx = idx_list.index(chg_pt_ts)
			
			# find freq immediately to the left and right of the chg pt 
			left_freq, rt_freq = None, None
			if chg_pt_idx > 0:
				left_freq = self.vfd_scheds.iat[chg_pt_idx-1, vfd_id]
			if chg_pt_idx < len(idx_list) - 1:
				rt_freq = self.vfd_scheds.iat[chg_pt_idx+1, vfd_id]
			
			start_idx, end_idx = None, None
			val = self.vfd_scheds.at[chg_pt_ts, vfd_id]

			if shift_type == self.LEFT:
				# copy the value to the left
				start_idx = chg_pt_ts - shift_mag
				end_idx = chg_pt_ts
			
			elif shift_type == self.RIGHT:
				# copy value to right
				start_idx = chg_pt_ts
				end_idx = chg_pt_ts + shift_mag
				# copy value just before the change chg pt
				val = left_freq
			
			elif shift_type == self.DOWN:
				# change pt can be beginning or the end of a plateau
				# if the value at the change pt is lower than the value
				# before it, the shift down is applied to the left of the
				# change pt and vice versa
				
				# do not assume contiguous index ts values
				if left_freq and left_freq > val and chg_pt:
					end_idx = idx_list[chg_pt_idx-1]
					start_idx = chg_pt_list[chg_pt-1]
					val = left_freq - self.THRESHOLD_CHANGE

				elif rt_freq and rt_freq > val and chg_pt < len(chg_pt_list) - 1:
					# this case will likely never happen because of the
					# way change pts are defined unless there are two consecutive
					# change pts, one time interval apart
					start_idx = idx_list[chg_pt_idx+1]
					end_idx = chg_pt_list[chg_pt+1]
					val = rt_freq - self.THRESHOLD_CHANGE

				else:
					raise Exception('shift could not be executed')
			
			
			# copy data
			tmp_idx = start_idx
			td = dt.timedelta(minutes=options.forecast_granularity)
			while tmp_idx <= end_idx:
				if tmp_idx in idx_list:
					shifted_vfd_df.at[tmp_idx, vfd_id] = val
				tmp_idx += td
		
		return shifted_vfd_df



	def perform_shift(self, chg_pt, vfd_ids, options, lgr):
		""" shift selected change point for all selected VFDs 
		"""

		# choose shift type, uniformly among possible shifts
		shift_type = self.MOVES[np.random.randint(0, len(self.MOVES))]
		print 'shift type: %s' % shift_type

		failure_count = 0
		shift_mag = None
		try:
			# choose shift magnitude; must be <= 
			mul = self._custom_round(np.random.gamma(0.5, 1))
			if not mul:
				mul = 1
			#print 'mul: %s' % mul
			shift_mag = mul*dt.timedelta(minutes=options.forecast_granularity) # in minutes
			print 'shift mag %s ' % shift_mag

			self._shift_sanity_check(chg_pt, vfd_ids, shift_type, shift_mag,
				options, lgr)

		except Exception, e:
			print e
			failure_count += 1
			if failure_count > 5:
				raise
			

		# execute shift
		return self.execute_shift(shift_mag, shift_type, chg_pt,
			vfd_ids, options, lgr)




	def rnd_shift(self, options, lgr, vfd_ids=None, change_pt_id=None):
		"""
			for all VFDs in vfd_ids, choose a shift from among
			left/right/down, apply the change to the schedule and
			return the new schedule
			change_pt_id is the the change point to consider moving
		"""
		
		# find vfds to consider
		vfd_id_list = range(0, self.vfd_scheds.shape[1])
		if vfd_ids:
			vfd_id_list = vfd_ids
		
		print 'vfd id list: %s' % vfd_id_list
		
		# find change point to shift
		chg_pt = self.select_change_point(change_pt_id, vfd_id_list)
		print 'selected chg pt: %s' % chg_pt

		# perform shift
		return self.perform_shift(chg_pt, vfd_id_list, options, lgr)


	def plot_vfd_sched(self, df, df_shifted, vfd_id, file_name):
		""" plt vfd sched """
		
		x = self.dt64_to_dt(list(df.index.values))
		
		
		
		print df.iloc[:,0]
		plot(x, df.iloc[:,0], 'g^', x, df_shifted.iloc[:,1], 'r-')

		xlabel('time')
		ylabel('rpm')
		title('vfd %s sched' % vfd_id)
		grid(True)
		savefig(file_name)
		show()


def main(argv):
	""" test function """

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

	run_ts = dt.datetime.now()
	lgr.info('run time: %s' % run_ts)

	#print sample_vfd_data_dict.items()
	sample_vdf_data_ord = OrderedDict(sorted(sample_vfd_data_dict.items(),
		key=lambda t: t[0]))
	#sample_vfd_data.append(sample_vdf_data_ord)

	vfd_df = pd.DataFrame(data=sample_vdf_data_ord.values(),
		index=sample_vdf_data_ord.keys())
	print vfd_df

	scen_gen = ScenarioGen(vfd_df)
	shifted_sched = scen_gen.rnd_shift(options, lgr)
	#print shifted_sched
	for vfd_id in range(vfd_df.shape[1]):
		scen_gen.plot_vfd_sched(vfd_df, shifted_sched, vfd_id,
			'shifted_vfd_%d_sched.png' % vfd_id)



if __name__ == '__main__':
	main(sys.argv)