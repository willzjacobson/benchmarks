#!/bin/env python

import common_rudin.utils as utils
import subprocess

import datetime


date_ranges = [[datetime.datetime(2012, 12, 8, 0, 0), datetime.datetime(2012, 12, 13, 0, 0)]]

for start_ts, end_ts in date_ranges:

	tmp_ts = start_ts
	td = datetime.timedelta(days=1)

	count = 0

	while tmp_ts <= end_ts:

		try:

			utils.create_child_proc(['python', 'predict_space_temp.py',
				str(tmp_ts.year), str(tmp_ts.month), str(tmp_ts.day),
				str(tmp_ts.hour), str(tmp_ts.minute)])

			# Run cross-validate after first step
			#if count == 1:
			utils.create_child_proc(['python',
				'../common_rudin/cross_validate.py'])

			tmp_ts += td
			count += 1

		except subprocess.CalledProcessError, e:

			print 'process failed %s' % str(e)
			#sys.exit(1)