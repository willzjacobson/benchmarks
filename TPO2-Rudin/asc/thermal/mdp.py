
import pyodbc
import sys
import optparse
import cfgparse

from common_rudin.common import log_from_config, setup, setup_cparser
import common_rudin.utils as utils

import datetime as dt

import numpy

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.mixture import GMM
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier

_module = 'thermal_mdp'


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
			File.write(str(X[i][-1]) + '\n')


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

		action_set_cardinality = 10

		a_gmm = GMM(action_set_cardinality )
		a_gmm.fit(action_matrix)

		self.actions_model = a_gmm

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


		if True:
			fig, ax = plt.subplots()
			ax.plot(timestamps[-800:], modes[-800:])
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

		for action in trans_prob_matrix:

			#fig, ax = plt.subplots()
			trans_prob_matrix[action] += 0.001
			for i in range(0, trans_prob_matrix[action].shape[0]):
				if numpy.sum(trans_prob_matrix[action][i]) == 0:
					continue
				trans_prob_matrix[action][i] /= numpy.sum(trans_prob_matrix[action][i])
			#ax.matshow(trans_prob_matrix[action])
			#plt.show()


		self.transProbMatrix = trans_prob_matrix


		#for i in range(0, 10):
		#	self.randomScenario()


		#for i in range(0, 10):
		#	self.backward_induction(int(numpy.random.rand()*len(self.states)))

		self.backward_induction(-1)



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
		b = []

		self.costs = numpy.random.rand(len(centroids), 2) * 0

		for pointname in self.state_pointnames: 
			if "TEMSPA" in pointname:
				a.append(0)
				b.append(1)

			else:
				a.append(1)
				b.append(0)

		a = numpy.array(a)
		b = numpy.array(b) 

		for i in xrange(len(centroids)):
			mean = centroids[i]
			energy_vector = numpy.sum(mean*a)

			temp_vector = (mean*b - 74)*(mean*b - 74)*(mean*b - 74)*(mean*b - 74)*b
		
			#temp_vector = numpy.sqrt((mean*b - 74)*(mean*b - 74)*b)
			#temp_vector = temp_vector-4 + numpy.abs(temp_vector-4)
			#temp_vector = numpy.sum(temp_vector * temp_vector)

			#print temp_vector
			temp_vector = numpy.sum(temp_vector)
			self.costs[i, 0] = energy_vector*1 + temp_vector*0
			self.costs[i, 1] = energy_vector*0 + temp_vector*1


		return self.costs.T[alpha]


	def scenario(self, last_state, action_sequence, last_dt):

		last_state = numpy.matrix(last_state)

		scenario = []
		rewards = []

		last_minute = last_dt.hour * 60 + last_dt.minute

		last_state = numpy.matrix(last_state)
		for a in action_sequence:
			scenario.append(numpy.array(last_state[0]))

			rewards.append(numpy.sum(numpy.array(last_state[0]) * self.cost(last_minute)))
			last_minute += 15

			last_state = last_state * numpy.matrix(self.transProbMatrix[a])

		fig, ax = plt.subplots()	
		scenario = numpy.array(scenario)
		D = self.reverse(scenario)
		dt_list = [last_dt]
		for i in xrange(len(D)-1):
			dt_list.append(dt_list[-1] + dt.timedelta(0, 15*60))

		for y in D.T:
			ax.plot(dt_list, y)

		ax.plot(dt_list, rewards, '--')

		plt.show()



	def randomScenario(self):

		last = numpy.matrix(self.states[-1])	

		actions = range(0, len(self.transProbMatrix))

		n = 24 * 4 * 2
		random_cursor = int(numpy.random.rand() * len(self.actions) - n)

		action_sequence = numpy.array(self.actions[random_cursor:random_cursor + n])
		
		last_state = self.states[random_cursor]
		#base_minute = self.dataframe.timestamps[random_cursor].hour * 60 + self.dataframe.timestamps[random_cursor].minute
		base_dt = self.dataframe.timestamps[random_cursor]

		self.scenario(last_state, action_sequence, base_dt)


	def backward_induction(self, state_index):


		l = self.dataframe.timestamps[state_index]
		l = l.hour * 60 + l.minute
		base_minute = l + 24 * 60

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
					value = numpy.sum(self.transProbMatrix[a][s] * (self.cost((base_minute - i*15)%24*60) + gamma * v_star.T[i-1]))

					if  value < v_star[s, i]:
						v_star[s, i] = value
						a_star[s, i] = a

		#print v_star
		#print a_star

		#self.scenario(self.states[state_index], a_star[numpy.argmax(self.states[state_index])][::-1], self.dataframe.timestamps[state_index])

		current_state = numpy.random.rand(len(state_set)) * 0 + 1
		for s in state_set:
			action_sequence = []
			state_sequence = []
			current_state = numpy.random.rand(len(state_set)) * 0
			current_state[s] = 1
			for i in range(0, len(a_star.T)): 
				maxstate = numpy.argmax(current_state)
				state_sequence.append(maxstate)
				action = a_star[maxstate, i]
				action_sequence.append(action)
				current_state = numpy.matrix(current_state) * numpy.matrix(self.transProbMatrix[action])
				current_state = numpy.array(current_state)
				
			#self.scenario(self.states[state_index], action_sequence, self.dataframe.timestamps[state_index])
			r = int(numpy.random.rand()*(len(self.actions)-24*4))
			self.scenario(self.states[state_index], self.actions[r:r+24*4], self.dataframe.timestamps[state_index])
			#self.scenario(self.states[state_index], numpy.floor(numpy.random.rand(90)*len(action_set)), self.dataframe.timestamps[state_index])
			#print action_sequence
			#print state_sequence

##############################

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
	
	#mod_optgroup = oparser.add_option_group(_module)
	#mod_cfggroup = cparser.add_option_group(_module)
	#add_config_options(mod_optgroup, mod_cfggroup)

	options, args = cparser.parse(oparser, argv)

	lgr = log_from_config(options, _module)
	lgr.info('*** %s starting up' % _module)

	arg_count = len(args)

	run_ts = dt.datetime.now()
	lgr.info('run time: %s' % run_ts)

	# determine start time
	run_as_of_ts = None
	if arg_count == 1:
		run_as_of_ts = run_ts
	elif arg_count == 6:
		int_args = map(int, args[1:])
		run_as_of_ts = dt.datetime(int_args[0], int_args[1], int_args[2],
			int_args[3], int_args[4])
	else:
		lgr.critical(args)
		oparser.error("incorrect number of arguments")

	run_as_of_ts = utils.adjust_ts(run_as_of_ts,
			options.forecast_granularity, options, lgr)
	run_dt = run_as_of_ts.date()
	lgr.info('start time: %s, start date = %s' % (run_as_of_ts, run_dt))
	data_length_td = dt.timedelta(days=120)
	data_start_dt = run_dt - data_length_td

	# get building ids
	building_ids = utils.parse_value_list(options.building_ids)

	reinstantiate_cparser = False
	for bldg_idx, building_id in enumerate(building_ids):

		if bldg_idx != 0:
			reinstantiate_cparser = True
		options = utils.load_bldg_config(building_id, oparser, cparser, argv,
			options, lgr, reinstantiate_cparser)

		d = DatabaseInterface(options.building_db_server, options.building_db,
			options.db_user, options.db_pwd)
		s = []
		s += d.get_bms_series(options.fan_table, data_start_dt, run_dt)
		s += d.get_bms_series(options.space_temp_tablename_format,
			data_start_dt, run_dt)
		s += d.get_bms_series(options.steam_demand_table,
			data_start_dt, run_dt)
		s += d.get_bms_series(options.electric_load_table, data_start_dt,
			run_dt)
		#s += d.get_bms_series("345---------000SECCNTPEOBUI---VAL001", '2014-01-01', '2014-10-01')


		d = DatabaseInterface(options.weather_db_server, options.weather_db,
			options.weather_db_user, options.weather_db_pwd)
		#s += d.get_generic_series("Observations_History", "Date", ["TempA", "DewPointA", "Humidity", "PressureA"], '2014-01-01', '2014-10-01')

		n = 7
		df = DataFrame()
		df.add_series(s)

		sa = StateAction(df)
		#sa.cluster(10, visual=True)
		sa.cluster(10)
		sa.transition()

		#x = pca(df, n)
		#states, actions = cluster(df.X, df.pointnames, df.timestamps, 30, visual=True)
		#cluster(x, df.pointnames[:n], df.timestamps, 15)
		#transition(df, states)
		#vis(df)

		#csv(X, pointnames, timestamps)
		#pca(X, pointnames, timestamps)
		#cluster(X, pointnames, timestamps)
		#cost(X, pointnames, timestamps)


if __name__ == '__main__':
	main(sys.argv)

