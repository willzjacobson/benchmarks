
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

	
	def get_bms_tables(self):

		cursor = self.connection.cursor()
		table_list = cursor.tables()
		t_list = []
		for t in table_list:
			if ("BMS" in t[2] or "BUI" in t[2]) and not("[" in t[2]) and not("TPO" in t[2]):
				t_list.append(str(t[2]))

		return t_list


	def __del__(self):
		self.connection.close()



class DataFrame:

	def __init__(self):
		self.raw = []
		self.X = []
		self.pointnames = []
		self.timestamps = []
		self.action_matrix = []
		self.states_matrix = []

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
			File.write(str(self.X[i][-1]) + '\n')


class StateAction:

	def __init__(self, df):

		self.dataframe = df
		self.states = None
		self.actions = None

		self.pca_model = None
		self.states_model = None
		self.actions_model = None

		self.actionSet = None

		self.costs = None

	def pca(self, X, pointnames, components, visual=False):

		timestamps = self.dataframe.timestamps
	
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

		self.pca_model = pca

		return x


	def cluster(self, dimensions, visual=False):

		X = self.dataframe.X
		pointnames = self.dataframe.pointnames
		timestamps = self.dataframe.timestamps

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
		self.state_pointnames = [pointnames[i] for i in state_indices]

		X = self.pca(X, self.state_pointnames, 10)

		gmm = GMM(n_components=n)
		gmm.fit(X)

		self.states_model = gmm

		action_set_cardinality = 8

		a_gmm = GMM(action_set_cardinality )
		a_gmm.fit(action_matrix)

		self.actions_model = a_gmm

		modes = gmm.predict(X)

		start = 0
		end = 0
		for i in range(0, len(timestamps)):
			if timestamps[i] > dt.datetime(2014, 8, 25) and not(start):
				start = i
			if timestamps[i] > dt.datetime(2014, 8, 30) and not(end):
				end = i

		print start
		print end

		if visual:
			fig, ax = plt.subplots()

			#start = len(timestamps) - 800
			#end = len(timestamps)

			segment_start = start 
			for i in range(start, end):
				#print i
				if modes[i] == modes[segment_start]:
					continue
				else:		
					for y in matrix:
						ax.plot(timestamps[segment_start:i], y[segment_start:i], color=colors[modes[segment_start]])
					segment_start = i

			plt.show()


		if True:
			fig, ax = plt.subplots()
			ax.plot(timestamps[start:end], modes[start:end])
			plt.show()


		for policy in a_gmm.means_:
			print numpy.floor(policy + 0.5)

		self.states, self.actions = gmm.predict_proba(X), a_gmm.predict(action_matrix)


	def transition(self):

		states = self.states
		actions = self.actions

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

		fig, axes = plt.subplots(2, 4, figsize=(12, 6), subplot_kw={'xticks':[], 'yticks':[]})

		for (ax, action) in zip(axes.flat, trans_prob_matrix):

			trans_prob_matrix[action] += 0.001
			for i in range(0, trans_prob_matrix[action].shape[0]):
				if numpy.sum(trans_prob_matrix[action][i]) == 0:
					continue
				trans_prob_matrix[action][i] /= numpy.sum(trans_prob_matrix[action][i])
			ax.imshow(trans_prob_matrix[action], interpolation='gaussian')
			
		plt.show()


		self.transProbMatrix = trans_prob_matrix


		for i in range(0, 10):
			self.randomScenario()

		#self.backward_induction()



	def reverse(self, states):

		centroids = self.states_model.means_

		recovered_data = numpy.matrix(states) * numpy.matrix(centroids)
		recovered_data = numpy.asarray(recovered_data)

		if self.pca_model != None:
			recovered_data = self.pca_model.inverse_transform(recovered_data)

		return recovered_data

	def cost(self, minute):

		hour = (minute/60) % 24
		open_hour = 7
		close_hour = 19

		alpha = 0
		if hour >= open_hour and hour < close_hour:
			alpha = 1

		if self.costs != None:
			return self.costs.T[alpha]

		if self.pca_model != None:
			centroids = self.pca_model.inverse_transform(self.states_model.means_)
		else:
			centroids = self.states_model.means_
		covars = self.states_model.covars_

		a = []

		self.costs = numpy.random.rand(len(centroids), 2) * 0

		for pointname in self.state_pointnames: 
			if "TEMSPA" in pointname:
				a.append(0)

			else:
				a.append(1)
		a = numpy.array(a)
		b = (a - 1) * (a - 1)

		for i in xrange(len(centroids)):
			mean = centroids[i]
			self.costs[i, 0] = numpy.sum(mean*a) + numpy.sum((mean*b - 75)*(mean*b - 75))*0
			self.costs[i, 1] = numpy.sum(mean*a) + numpy.sum((mean*b - 75)*(mean*b - 75))*.10


		return self.costs.T[alpha]


	def scenario(self, last_state, action_sequence, last_minute):

		last_state = numpy.matrix(last_state)

		scenario = []
		rewards = []

		last_state = numpy.matrix(last_state)
		for a in action_sequence:
			scenario.append(numpy.array(last_state[0]))

			rewards.append(numpy.sum(numpy.array(last_state[0]) * self.cost(last_minute)))
			last_minute += 15

			last_state = last_state * numpy.matrix(self.transProbMatrix[a])


		fig, ax = plt.subplots()	
		scenario = numpy.array(scenario)
		D = self.reverse(scenario)
		return D
		for y in D.T:
			ax.plot(range(0, len(y)), y, '--')

		#ax.plot(range(0, len(rewards)), rewards)

		plt.show()



	def randomScenario(self):

		last = numpy.matrix(self.states[-1])

	

		actions = range(0, len(self.transProbMatrix))

		n = 24 * 4 * 2
		random_cursor = int(numpy.random.rand() * len(self.actions) - n)

		action_sequence = numpy.array(self.actions[random_cursor:random_cursor + n])
		
		last_state = self.states[random_cursor]
		last_minute = self.dataframe.timestamps[random_cursor].hour * 60 + self.dataframe.timestamps[random_cursor].minute

		D = self.scenario(last_state, action_sequence, last_minute)
		RD = self.reverse(self.states[random_cursor:random_cursor + n])

		fig, ax = plt.subplots()
		for (y, ry) in zip(D.T, RD.T):
			rand_color = numpy.random.rand(3, 1)
			ax.plot(self.dataframe.timestamps[random_cursor:random_cursor+n], ry, color=rand_color)
			ax.plot(self.dataframe.timestamps[random_cursor:random_cursor+n], y, '--', color=rand_color)
		plt.show()


	def backward_induction(self):


		l = self.dataframe.timestamps[-1]
		l = l.hour * 60 + l.minute
		base_minute = l

		state_set = range(0, len(self.states_model.means_))
		action_set = range(0, len(self.actions_model.means_))

		horizon = range(0, 24 * 4)

		v_star = numpy.random.rand(len(state_set), len(horizon))*0
		a_star = numpy.random.rand(len(state_set), len(horizon))*0

		gamma = 1

		for i in horizon[1:]:
			for s in state_set:
				v_star[s, i] = numpy.inf
				for a in action_set:
					value = numpy.sum(self.transProbMatrix[a][s] * (self.cost(base_minute + i*15%24) + gamma * v_star.T[i-1]))
					print str(i) + " " + str(s) + " " + str(a) + " " + str(value)

					if  value < v_star[s, i]:
						v_star[s, i] = value
						a_star[s, i] = a

		#print v_star
		#print a_star

		self.scenario(self.states[-1], a_star[numpy.argmax(self.states[-1])], l)


##############################

d = DatabaseInterface("anderson.ldeo.columbia.edu", "345", "Hooshmand", "Breakit68")
s = []
#s += d.get_bms_series("345---------001BMSHVAFANLCP---VAL001", '2014-01-01', '2014-10-01')
#s += d.get_bms_series("345---------001BMSHVATEMSPA---VAL001", '2014-01-01', '2014-10-01')
#s += d.get_bms_series("345---------001BMSSTEMET------MVA001", '2014-01-01', '2014-10-01')
#s += d.get_bms_series("345---------001BMSELEMET------VAL001", '2014-01-01', '2014-10-01')
#s += d.get_bms_series("345---------000SECCNTPEOBUI---VAL001", '2014-01-01', '2014-10-01')
tables = d.get_bms_tables()
for table in tables:
	s += d.get_bms_series(table, '2013-01-01', '2014-10-01')

d = DatabaseInterface("anderson.ldeo.columbia.edu", "Weather", "Hooshmand", "Breakit68")
s += d.get_generic_series("Observations_History", "Date", ["TempA", "DewPointA", "Humidity", "PressureA"], '2013-01-01', '2014-10-01')

n = 7
df = DataFrame()
df.add_series(s)
df.csv()


##sa = StateAction(df)
##sa.cluster(30, visual=True)
##sa.transition()

#x = pca(df, n)
#states, actions = cluster(df.X, df.pointnames, df.timestamps, 30, visual=True)
#cluster(x, df.pointnames[:n], df.timestamps, 15)
#transition(df, states)
#vis(df)

#csv(X, pointnames, timestamps)
#pca(X, pointnames, timestamps)
#cluster(X, pointnames, timestamps)
#cost(X, pointnames, timestamps)


