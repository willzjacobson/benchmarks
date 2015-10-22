
import datetime as dt

import numpy
from scipy import interpolate
import bisect

import matplotlib.pyplot as plt

from sklearn.ensemble import ExtraTreesRegressor

class DataFrame:

	def __init__(self):
		self.raw = []
		self.X = []
		self.pointnames = []
		self.timestamps = []
		self.Type = []
		self.group = {}
		self.covarSize = 0
		self.pointSize = 0

		self.data_gaps = []
		self.data_gaps_index = []


	def set(self, X, pointnames, timestamps, group):

		self.X = X
		self.pointnames = pointnames
		self.timestamps = timestamps
		self.covarSize = len(pointnames)
		self.pointSize = len(timestamps)
		self.group = group


	def add_series(self, series, _from=None, _to=None, granularity=15):
		self.raw += series

		self.process(_from, _to, granularity)
		#self.normalize()


	def align(self):

		all_timestamps = []
		for [pointname, timestamps, values, group, discrete], i in zip(self.raw, xrange(len(self.raw))):
			all_timestamps += timestamps
			self.pointnames.append(pointname)
			try:
				self.group[group].append(i)
			except:
				self.group[group] = [i]
		all_timestamps = set(all_timestamps)
		all_timestamps = sorted(list(all_timestamps))
		T = len(all_timestamps)
		self.covarSize = len(self.pointnames)

		self.X = numpy.random.rand(T, self.covarSize)*0 - 9999

		tim_index = {}
		for t, i in zip(all_timestamps, xrange(T)):
			time_index[t] = i

		for [pointname, timestamps, values, group, discrete], i in zip(self.raw, xrange(len(self.raw))):
			for v, t in zip(timestamps, values):
				self.X[time_index[t], i] = v


	def refine(self, group, base_groups, max_flat_line = 20):

		refI = []
		for g in base_groups:
			refI += self.group[g]
		refI = sorted(list(set(refI)))

		refX = numpy.array([self.X.T[i] for i in refI]).T

		for i in self.group[group]:
			y = self.X.T[i]

			freezed_value = y[0]
			freezed_time = self.timestamps[0]
			freezed_index = 0
			
			gapI = []

			for t, v , j in zip(self.timestamps, y, xrange(self.pointSize)):

				if v != freezed_value:
					duration = t - freezed_time
					duration_flat_line = duration.days*24 + duration.seconds//3600
					if duration_flat_line >= max_flat_line: 	
						gapI += range(freezed_index, j)

					freezed_index = j
					freezed_value = v
					freezed_time = t

			validI = list(set(range(0, self.pointSize)).difference(set(gapI)))
			validY = numpy.array([y[k] for k in validI])
			validX = numpy.array([refX[k] for k in validI])
			gapX = numpy.array([refX[k] for k in gapI])
			est = ExtraTreesRegressor()
			est.fit(validX, validY)
			gapY = est.predict(gapX)

			for j, k in zip(gapI, xrange(len(gapY))):
				self.X[j, i] = gapY[k]
			

	def process(self, _from, _to, granularity):
		ud = self.raw 
		all_timestamps = set([])
		pointnames = []
		for [pointname, timestamps, values, _group, discrete], i in zip(ud, xrange(len(ud))):
			all_timestamps = all_timestamps.union(set(timestamps))
			pointnames.append(pointname)
			try:
				self.group[_group].append(i)
			except:
				self.group[_group] = [i]

			if discrete:
				self.Type.append('discrete')
			else:
				self.Type.append('continuous') 

		all_timestamps = sorted(list(all_timestamps))

		if _from == None and _to == None:
			base = min(all_timestamps)
			end = max(all_timestamps)

		else:
			base = _from
			end = _to

		timestamps = []
		timestamps_offset = []

		while True:
			base += dt.timedelta(0, 1)
			if base.minute % 15 == 0 and base.second == 0:
				break
		while True:
			end += dt.timedelta(0, 1)
			if end.minute %15 == 0 and end.second == 0:
				break

		current = base
		current_offset = 0

		while current <= end:
			timestamps.append(current)
			timestamps_offset.append(current_offset)
			current += dt.timedelta(0, granularity * 60)
			current_offset += granularity

		matrix = []

		for [pointname, ts, values, group, discrete] in ud:
			x = []
			for t in ts:
				offset = t-base
				x.append(offset.days * 24 * 60 + offset.seconds / 60)
			x = [timestamps_offset[0]] + x + [timestamps_offset[-1]]
			aug_values = [values[0]] + values + [values[-1]]

			#interpolated_values = numpy.interp(timestamps_offset, x, values)
			#matrix.append(list(interpolated_values))

			#function = interpolate.interp1d(x, aug_values, kind='linear')
			function = interpolate.interp1d(x, aug_values, kind='nearest')
			interpolated_values = function(timestamps_offset)

			nan_flag = numpy.nan in interpolated_values or numpy.inf in interpolated_values


			if discrete or nan_flag:
				#function = interpolate.interp1d(x, aug_values, kind='nearest')	
				function = interpolate.interp1d(x, aug_values, kind='zero')	
				interpolated_values = function(timestamps_offset)
				nan_flag = numpy.nan in interpolated_values or numpy.inf in interpolated_values

			if nan_flag:
				print "NAN value for {0}".format(pointname)
	

			matrix.append(list(interpolated_values))

		matrix = numpy.matrix(matrix)
		matrix = numpy.asarray(matrix)
		X = matrix.transpose()
		X = numpy.asarray(X)

		self.X = X
		self.pointnames = pointnames
		self.timestamps = timestamps
		self.pointSize = len(self.timestamps)
		self.covarSize = len(self.pointnames)

		time_covar = numpy.array([[t.hour*60 + t.minute, t.weekday()] for t in self.timestamps])
		self.X = numpy.concatenate((self.X, time_covar), axis=1)
		self.pointnames.append('minute')
		self.pointnames.append('weekday')
		self.group['time'] = [self.covarSize, self.covarSize+1]
		self.covarSize += 2
		self.Type += ['continuous', 'continuous']


	def gaps(self):
		data_gaps = []
		for cov in self.raw:
			timestamps = cov[1]
			if len(timestamps) < self.pointSize/4:
				print "Too few datapoints for " + cov[0]
				continue
			if timestamps != []:
				delta = self.timestamps[0] - timestamps[0]
				if delta.days > 1 or (delta.days < 1 and delta.seconds > 3600 * 2):
					interval = (self.timestamps[0], timestamps[0])
					data_gaps.append(interval)

			for i in range(1, len(timestamps)):
				delta = timestamps[i] - timestamps[i-1]
				if delta.days > 1 or (delta.days < 1 and delta.seconds > 3600 * 2):
					interval = (timestamps[i-1], timestamps[i])
					data_gaps.append(interval)

			if timestamps != []:
				delta = timestamps[-1] - self.timestamps[-1] 
				if delta.days > 1 or (delta.days < 1 and delta.seconds > 3600 * 2):
					interval = (timestamps[i-1], self.timestamps[-1])
					data_gaps.append(interval)

		data_gaps = set(data_gaps)
		data_gaps = list(data_gaps)
		data_gaps.sort()

		corrupt = []
		for i in xrange(len(data_gaps)):
			corrupt.append(0)


		for i in xrange(len(data_gaps)):
			print str(data_gaps[i][0]) + " to " + str(data_gaps[i][1])
		print '--------------------'

		for i in xrange(len(data_gaps)-1):
			if data_gaps[i][1] >= data_gaps[i+1][0]:
				if data_gaps[i][1] < data_gaps[i+1][1]:
					data_gaps[i+1] = (data_gaps[i][0], data_gaps[i+1][1])
					corrupt[i] = 1
				else:
					data_gaps[i+1] = (data_gaps[i][0], data_gaps[i+1][0])
					corrupt[i] = 1

		for i in xrange(len(data_gaps)):
			print str(data_gaps[i][0]) + " to " + str(data_gaps[i][1]) + ' ' + str(corrupt[i])
		print '--------------------'


		print 'For the following time intervals there is partial or no data vailable.'
		for i in xrange(len(data_gaps)):
			if not(corrupt[i]):
				self.data_gaps.append(data_gaps[i])
				print str(data_gaps[i][0]) + " to " + str(data_gaps[i][1]) 
		print '--------------------'

		self.data_gaps_index = []

		for g in self.data_gaps:
			i1 = bisect.bisect_left(self.timestamps, g[0])
			i2 = bisect.bisect_right(self.timestamps, g[1])
			self.data_gaps_index.append((i1, i2))
			print self.data_gaps_index[-1]


	def plot(self, groups = []):

		if groups == []:
			groups = self.group.keys()

		if not(isinstance(groups, list)):
			groups = [groups]

		fig, ax = plt.subplots()
		for g in groups:
			for i in self.group[g]:
				ax.plot(self.timestamps, self.X.T[i])
		plt.show()
	
	def normalize(self):

		matrix = numpy.matrix(self.X)
		matrix = matrix.transpose()
		matrix = numpy.asarray(matrix)

		for i in xrange(len(matrix)):
			matrix[i] -= numpy.min(matrix[i])
			matrix[i] /= numpy.max(matrix[i])

		matrix = numpy.matrix(matrix)
		matrix = matrix.transpose()
		self.X = matrix


	def csv(self):
		File = open('snapshot.csv', 'w')
		File.write("Timestamp, ")
		for i in range(0, len(self.pointnames)-1):
			File.write(self.pointnames[i] + ", ")
		File.write(self.pointnames[-1] + '\n')

		for i in range(0, len(self.X)):
			File.write(str(self.timestamps[i]) + ", ")
			for j in range(0, len(self.X[i])-1):
				File.write(str(self.X[i][j]) + ", ")
			File.write(str(self.X[i][-1]) + '\n')


	def subset(self, _from, _to, groups=[]):
		
		df = DataFrame()

		fi = bisect.bisect_left(self.timestamps, _from)
		ti =bisect.bisect_right(self.timestamps, _to)

		df.X = self.X[fi:ti]
		df.pointnames = self.pointnames
		df.timestamps = self.timestamps[fi:ti]
		df.Types = self.Type
		df.group = self.group
		df.covarSize = self.covarSize
		df.pointSize = self.pointSize

		df.data_gaps = []
		df.data_gaps_index = []

		return df


	def merge(self, df, override=True):

		if not(self.pointnames == df.pointnames):
			return

		if override:
			for i in reversed(xrange(len(self.timestamps))):
				if self.timestamps[i] > df.timestamps[0]:
					continue
				else:
					self.timestamps = self.timestamps[:i+1] + df.timestamps
					self.X = numpy.concatenate((self.X[:i+1], df.X), axis=0)
					break

		else:
			self.timestamps += df.timestamps
			self.X = numpy.concatenate((self.X, df.X), axis=0)

		sorted_index = [i[1] for i in sorted(zip(self.timestamps, xrange(len(self.timestamps))))]
		self.timestamps = [self.timestamps[i] for i in sorted_index]
		self.X = numpy.array([self.X[i] for i in sorted_index])

		self.pointSize = len(self.timestamps)

