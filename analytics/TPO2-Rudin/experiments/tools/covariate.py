
import pyodbc

import datetime as dt

import numpy

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.mixture import GMM
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier


class DatabaseInterface:

	def __init__(self, server, database, db_uid, db_pwd):
		self.connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(server, database, db_uid, db_pwd)) 

	def get_bms_series(self, tables, _from, _to):
		
		cursor = self.connection.cursor()
		if not(isinstance(tables, list)):
			tables = [tables]

		unprocessed_dataset = []
		for table in tables:

			query = "SELECT DISTINCT ZONE, FLOOR, QUADRANT, EQUIPMENT_NO FROM [{0}] WHERE TIMESTAMP > '{1}' AND TIMESTAMP < '{2}'"
			query = query.format(table, _from, _to)
			cursor.execute(query)
			pointnames = cursor.fetchall()
	
			for p in pointnames:
				pointname = table[:3] + str(p.ZONE) + str(p.FLOOR) + str(p.QUADRANT) + table[12:27] + str(p.EQUIPMENT_NO) + table[30:]
				query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE ZONE='{1}' AND FLOOR='{2}' AND QUADRANT='{3}' AND EQUIPMENT_NO='{4}' AND TIMESTAMP > '{5}' AND TIMESTAMP < '{6}' ORDER BY TIMESTAMP"
				query = query.format(table, p.ZONE, p.FLOOR, p.QUADRANT, p.EQUIPMENT_NO, _from, _to)
				cursor.execute(query)
				entries = cursor.fetchall()
				print pointname + ": " + str(len(entries)) + " points"
				x = []
				y = []
				for e in entries:
					x.append(e.TIMESTAMP)
					y.append(e.VALUE)
				unprocessed_dataset.append([pointname, x, y])

		return unprocessed_dataset
		cursor.close()

	def get_generic_series(self, table, time_column, value_columns, _from, _to):
		
		cursor = self.connection.cursor()
		unprocessed_dataset = []

		for value_column in value_columns:
			pointname = table + "_" + value_column
			query = "SELECT {0} AS TIMESTAMP, {1} AS VALUE FROM [{2}] WHERE {3} > '{4}' AND {5} < '{6}' ORDER BY {7}"
			query = query.format(time_column, value_column, table, time_column, _from, time_column, _to, time_column) 
			cursor.execute(query)
			entries = cursor.fetchall()
			print pointname + ": " + str(len(entries)) + " points"
			x = []
			y = []
			for e in entries:
				ts = str(e.TIMESTAMP)
				timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
				x.append(timestamp)
				y.append(e.VALUE)
			unprocessed_dataset.append([pointname, x, y])

		return unprocessed_dataset

		cursor.close()


	def __del__(self):
		self.connection.close()

class DataFrame:

	def __init__(self):
		self.raw = []

		self.X = []
		self.pointnames = []
		self.timestamps = []

	def add_series(self, series):
		self.raw += series

		self.process(15)
		#self.scale()

	def process(self, granularity):
		ud = self.raw 
		all_timestamps = set([])
		pointnames = []
		for [pointname, timestamps, values] in ud:
			all_timestamps = all_timestamps.union(set(timestamps))
			pointnames.append(pointname)

		all_timestamps = sorted(list(all_timestamps))

		base = min(all_timestamps)
		end = max(all_timestamps)

		timestamps = []
		timestamps_offset = []

		current = base
		current_offset = 0
		while True:
			base += dt.timedelta(0, 1)
			if base.minute % 15 == 0:
				break
		while current <= end:
			timestamps.append(current)
			timestamps_offset.append(current_offset)
			current += dt.timedelta(0, granularity * 60)
			current_offset += granularity

		matrix = []

		for [pointname, ts, values] in ud:
			x = []
			for t in ts:
				offset = t-base
				x.append(offset.days * 24 * 60 + offset.seconds / 60)

			interpolated_values = numpy.interp(timestamps_offset, x, values)
			matrix.append(list(interpolated_values))

		matrix = numpy.matrix(matrix)
		matrix = numpy.asarray(matrix)
		X = matrix.transpose()
		X = numpy.asarray(X)

		self.X = X
		self.pointnames = pointnames
		self.timestamps = timestamps

	
	def scale(self):

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
			File.write(str(X[i][-1]) + '\n')


class StateActionMatrix:

	def __init__(self, dataframe):

		X = dataframe.X
		X = X.T


def pca(dataframe, components, visual=False):

	X = dataframe.X
	pointnames = dataframe.pointnames
	timestamps = dataframe.timestamps
	
	matrix = numpy.matrix(X)
	matrix = matrix.transpose()
	matrix = numpy.asarray(matrix)

	nrange = range(2, len(matrix))
	errors = []
	
	pca = PCA(n_components=components)

	pca.fit(X)
	eigenvectors = pca.components_
	eigenvalues = pca.explained_variance_ratio_

	if visual:
		ncovariates = len(pointnames)
		fig, ax = plt.subplots()

		for i in xrange(components):
			ax.bar(xrange(ncovariates), eigenvalues[i] * numpy.abs(eigenvectors[i]), color=numpy.random.rand(3, 1))

		plt.xlabel("Covariate Number")
		plt.ylabel("Weighted Covariate Coefficient")
		plt.title("PCA Analysis With " + str(components) + " Components")
		plt.legend(["component 1", "component 2", "component 3", "component 4", "component 5", "component 6", "component 7"])
		#plt.xticks(numpy.array(xrange(ncovariates))+1/2., pointnames)
		plt.show()
	
	x = pca.transform(X)
	return x

def cluster(X, pointnames, timestamps, dimensions, visual=False):

	matrix = X.T

	n = dimensions
	colors = numpy.random.rand(n, 3)


	state_indices = []
	action_indices = []
	for i in xrange(len(pointnames)):
		if "FANLCP" in pointnames[i]:
			action_indices.append(i)
		else:
			state_indices.append(i)
	
	action_matrix = numpy.array([matrix[i] for i in action_indices])
	action_matrix = action_matrix.T
	X = numpy.array([matrix[i] for i in state_indices])
	X = X.T

	gmm = GMM(n_components=n)
	gmm.fit(X)


	a_gmm = GMM(10)
	a_gmm.fit(action_matrix)

	modes = gmm.predict(X)
	
	
	if visual:
		fig, ax = plt.subplots()

		start = len(timestamps) - 800
		segment_start = start 
		for i in range(start, len(timestamps)):
			#print i
			if modes[i] == modes[segment_start]:
				continue
			else:		
				for y in matrix:
					ax.plot(timestamps[segment_start:i], y[segment_start:i], color=colors[modes[segment_start]])
				segment_start = i

		plt.show()


	return gmm.predict_proba(X), a_gmm.predict(action_matrix)


def transition(df, states):

	print "modeling states transition probability"
	n_clusters = states.shape[1]
	#trans_prob_matrix = numpy.random.rand(n_clusters, n_clusters)*0
	trans_prob_matrix = {}
	normalizing_consts = numpy.random.rand(n_clusters)*0

	for i in range(0, len(states)-1):
		for j in xrange(len(states[i])):
			try:
				trans_prob_matrix[actions[i]][j] += states[i][j] * states[i+1]
			except:
				trans_prob_matrix[actions[i]] = numpy.random.rand(n_clusters, n_clusters)*0

	for action in trans_prob_matrix:

		fig, ax = plt.subplots()
		ax.matshow(trans_prob_matrix[action])
		plt.show()
		#plt.colorbar()


def vis(df):

	fig, ax = plt.subplots()
	for y in df.X.T:
		ax.plot(df.timestamps, y)

	plt.show()

d = DatabaseInterface("anderson.ldeo.columbia.edu", "345", "Hooshmand", "Breakit68")
s = []
s += d.get_bms_series("345---------001BMSHVAFANLCP---VAL001", '2014-07-01', '2014-09-01')
s += d.get_bms_series("345---------001BMSHVATEMSPA---VAL001", '2014-07-01', '2014-09-01')
s += d.get_bms_series("345---------001BMSSTEMET------MVA001", '2014-07-01', '2014-09-01')
s += d.get_bms_series("345---------001BMSELEMET------VAL001", '2014-07-01', '2014-09-01')
s += d.get_bms_series("345---------000SECCNTPEOBUI---VAL001", '2014-07-01', '2014-09-01')


d = DatabaseInterface("anderson.ldeo.columbia.edu", "Weather", "Hooshmand", "Breakit68")
s += d.get_generic_series("Observations_History", "Date", ["TempA", "DewPointA", "Humidity", "PressureA"], '2014-07-01', '2014-09-01')

n = 7
df = DataFrame()
df.add_series(s)

SAM = StateActionMatrix(df)

x = pca(df, n)
states, actions = cluster(df.X, df.pointnames, df.timestamps, 30)
#cluster(x, df.pointnames[:n], df.timestamps, 15)
transition(df, states)
#vis(df)

#csv(X, pointnames, timestamps)
#pca(X, pointnames, timestamps)
#cluster(X, pointnames, timestamps)
#cost(X, pointnames, timestamps)


