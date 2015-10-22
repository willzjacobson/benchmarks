
import pyodbc
import numpy
import datetime as dt



class DatabaseInterface:

	def __init__(self, server, database, db_uid, db_pwd):
		self.connection = pyodbc.connect("DRIVER={SQL SERVER};" + "SERVER={0};DATABASE={1};UID={2};PWD={3}".format(server, database, db_uid, db_pwd)) 
	#_keys = [(Floor_1, Quadrant_1), (Floor_2, Quadrant_2), ..., (Floor_n, Quadrant_n)]
	def get_bms_series(self, tables, _from, _to, _group='ALL', _discrete=False, _keys=None, _domain=(-numpy.inf, numpy.inf), last=False):
		
		cursor = self.connection.cursor()
		if not(isinstance(tables, list)):
			tables = [tables]

		unprocessed_dataset = []
		for table in tables:

			query = "SELECT DISTINCT ZONE, FLOOR, QUADRANT, EQUIPMENT_NO FROM [{0}] WHERE TIMESTAMP >= '{1}' AND TIMESTAMP <= '{2}'"
			query = query.format(table, _from, _to)
			cursor.execute(query)
			pointnames = cursor.fetchall()
	
			for p in pointnames:
				pointname = table[:3] + str(p.ZONE) + str(p.FLOOR) + str(p.QUADRANT) + table[12:27] + str(p.EQUIPMENT_NO) + table[30:]
				query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE ZONE='{1}' AND FLOOR='{2}' AND QUADRANT='{3}' AND EQUIPMENT_NO='{4}' AND TIMESTAMP > '{5}' AND TIMESTAMP < '{6}' ORDER BY TIMESTAMP"
				key_flag = True
				if _keys != None:
					key_flag = False
					for _floor, _quadrant in _keys:
						if str(p.FLOOR) == _floor and str(p.QUADRANT) == _quadrant:
							key_flag = True
							break
				if not(key_flag):
					continue
				query = query.format(table, p.ZONE, p.FLOOR, p.QUADRANT, p.EQUIPMENT_NO, _from, _to)
				cursor.execute(query)
				entries = cursor.fetchall()
				print pointname + ": " + str(len(entries)) + " points"
				x = []
				y = []
				for e in entries:
					if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):
						continue 
					#x.append(e.TIMESTAMP)
					ts = str(e.TIMESTAMP)
					timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
					x.append(timestamp)
					y.append(e.VALUE)

				# dealing with void
				if last:	
					timestamp = dt.datetime.strptime(str(_to)[:19], "%Y-%m-%d %H:%M:%S")
					unprocessed_dataset.append([pointname, [timestamp], [y[-1]], _group, _discrete])
				else:
					unprocessed_dataset.append([pointname, x, y, _group, _discrete])

		cursor.close()
		return unprocessed_dataset
	
	# ag2818: for series with data overlapping in time
	def get_overlapping_series(self, tables, _from, _to, _group='ALL',
			_discrete=False, _keys=None, _domain=(-numpy.inf, numpy.inf),
			last=False):
		
		cursor = self.connection.cursor()
		if not(isinstance(tables, list)):
			tables = [tables]

		unprocessed_dataset = []
		for table in tables:

			query = "SELECT DISTINCT ZONE, FLOOR, QUADRANT, EQUIPMENT_NO FROM [{0}] WHERE TIMESTAMP >= '{1}' AND TIMESTAMP <= '{2}'"
			query = query.format(table, _from, _to)
			cursor.execute(query)
			pointnames = cursor.fetchall()
	
			for p in pointnames:
				pointname = table[:3] + str(p.ZONE) + str(p.FLOOR) + str(p.QUADRANT) + table[12:27] + str(p.EQUIPMENT_NO) + table[30:]
				#query = "SELECT TIMESTAMP, VALUE FROM [{0}] WHERE ZONE='{1}' AND FLOOR='{2}' AND QUADRANT='{3}' AND EQUIPMENT_NO='{4}' AND TIMESTAMP > '{5}' AND TIMESTAMP < '{6}' ORDER BY TIMESTAMP"
				query = """SELECT t1.TIMESTAMP, t1.VALUE
					FROM [{0}] t1,
						(SELECT  MAX(Runtime) Runtime, TIMESTAMP
							FROM [{0}]
							WHERE Floor = '{2}' AND Quadrant = '{3}'
								AND EQUIPMENT_NO = '{4}'
							GROUP BY TIMESTAMP) t2
					WHERE t1.Floor = '{2}' AND t1.Quadrant = '{3}'
						AND t1.EQUIPMENT_NO = '{4}'
						AND t1.Runtime = t2.Runtime
						AND t1.TIMESTAMP = t2.TIMESTAMP
						AND t1.TIMESTAMP > '{5}' AND t1.TIMESTAMP < '{6}'
					ORDER BY t1.TIMESTAMP"""
				key_flag = True
				if _keys != None:
					key_flag = False
					for _floor, _quadrant in _keys:
						if str(p.FLOOR) == _floor and str(p.QUADRANT) == _quadrant:
							key_flag = True
							break
				if not(key_flag):
					continue
				query = query.format(table, p.ZONE, p.FLOOR, p.QUADRANT, p.EQUIPMENT_NO, _from, _to)
				cursor.execute(query)
				entries = cursor.fetchall()
				print pointname + ": " + str(len(entries)) + " points"
				x = []
				y = []
				for e in entries:
					if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):
						continue 
					#x.append(e.TIMESTAMP)
					ts = str(e.TIMESTAMP)
					timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
					x.append(timestamp)
					y.append(e.VALUE)

				# dealing with void
				if last:	
					timestamp = dt.datetime.strptime(str(_to)[:19], "%Y-%m-%d %H:%M:%S")
					unprocessed_dataset.append([pointname, [timestamp], [y[-1]], _group, _discrete])
				else:
					unprocessed_dataset.append([pointname, x, y, _group, _discrete])

		cursor.close()
		return unprocessed_dataset
	


	def get_generic_series(self, (table, table_alias), time_column, value_columns, _from, _to, _group='ALL', _discrete=False, _domain=(-numpy.inf, numpy.inf)):
		
		cursor = self.connection.cursor()
		unprocessed_dataset = []

		for value_column, value_column_alias in value_columns:
			pointname = table_alias + "_" + value_column_alias
			query = "SELECT {0} AS TIMESTAMP, {1} AS VALUE FROM [{2}] WHERE {3} >= '{4}' AND {5} <= '{6}' ORDER BY {7}"
			query = query.format(time_column, value_column, table, time_column, _from, time_column, _to, time_column) 
			cursor.execute(query)
			entries = cursor.fetchall()
			print pointname + ": " + str(len(entries)) + " points"
			x = []
			y = []
			for e in entries:
				if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):
					continue
				ts = str(e.TIMESTAMP)
				timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
				x.append(timestamp) 
				y.append(e.VALUE)
			unprocessed_dataset.append([pointname, x, y, _group, _discrete])


		cursor.close()
		return unprocessed_dataset

	def get_bms_forecast(self, (table, table_alias), meta_time_column, time_column, value_columns, _time, _before, _group='ALL', _discrete=False, _domain=(-numpy.inf, numpy.inf)):
		
		cursor = self.connection.cursor()
		unprocessed_dataset = []

		for value_column, value_column_alias in value_columns:
			pointname = table_alias + "_" + value_column_alias
			query = "SELECT {0} AS TIMESTAMP, {1} AS VALUE FROM ([{2}] a INNER JOIN (SELECT MAX({3}) as most_recent FROM [{4}] WHERE {5} <= '{6}') b ON a.{7} = b.most_recent) WHERE {8} < '{9}' ORDER BY {10}" 
			query = query.format(time_column, value_column, table, meta_time_column, table, meta_time_column, _time, meta_time_column, time_column, _before, time_column) 
			
			cursor.execute(query)
			entries = cursor.fetchall()
			print pointname + ": " + str(len(entries)) + " points"
			x = []
			y = []
			for e in entries:
				if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):	
					continue
				ts = str(e.TIMESTAMP)
				timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
				x.append(timestamp)
				y.append(e.VALUE)
			unprocessed_dataset.append([pointname, x, y, _group, _discrete])

		cursor.close()
		return unprocessed_dataset


	def commit_bms_series(self, table, time, pointname, timestamps, values):

		cursor = self.connection.cursor()
		zone = pointname[3:6]
		floor = pointname[6:9]
		quadrant = pointname[9:12]
		equipment = pointname[27:30]

		for timestamp, value in zip(timestamps, values):
			query = "INSERT INTO [{0}] (ZONE, FLOOR, QUADRANT, EQUIPMENT_NO, TIMESTAMP, VALUE, RUNTIME) VALUES('{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}')"
			query = query.format(table, zone, floor, quadrant, equipment, str(timestamp)[:19], value, time)	
			cursor.execute(query)

		cursor.commit()
		cursor.close()



	def get_forecast_series(self, (table, table_alias), meta_time_column, time_column, value_columns, _time, _before, _group='ALL', _discrete=False, _domain=(-numpy.inf, numpy.inf)):
		
		cursor = self.connection.cursor()
		unprocessed_dataset = []

		for value_column, value_column_alias in value_columns:
			pointname = table_alias + "_" + value_column_alias
			query = "SELECT {0} AS TIMESTAMP, {1} AS VALUE FROM ([{2}] a INNER JOIN (SELECT MAX({3}) as most_recent FROM [{4}] WHERE {5} <= '{6}') b ON a.{7} = b.most_recent) WHERE {8} < '{9}' ORDER BY {10}" 
			query = query.format(time_column, value_column, table, meta_time_column, table, meta_time_column, _time, meta_time_column, time_column, _before, time_column) 
			
			cursor.execute(query)
			entries = cursor.fetchall()
			print pointname + ": " + str(len(entries)) + " points"
			x = []
			y = []
			for e in entries:
				if not(e.VALUE > _domain[0] and e.VALUE < _domain[1]):	
					continue
				ts = str(e.TIMESTAMP)
				timestamp = dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
				x.append(timestamp)
				y.append(e.VALUE)
			unprocessed_dataset.append([pointname, x, y, _group, _discrete])

		cursor.close()
		return unprocessed_dataset


	def commit_bms_series(self, table, time, pointname, timestamps, values):

		cursor = self.connection.cursor()
		zone = pointname[3:6]
		floor = pointname[6:9]
		quadrant = pointname[9:12]
		equipment = pointname[27:30]

		for timestamp, value in zip(timestamps, values):
			query = "INSERT INTO [{0}] (ZONE, FLOOR, QUADRANT, EQUIPMENT_NO, TIMESTAMP, VALUE, RUNTIME) VALUES('{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}')"
			query = query.format(table, zone, floor, quadrant, equipment, str(timestamp)[:19], value, time)	
			cursor.execute(query)

		cursor.commit()
		cursor.close()


	def commit_recommendation(self, table, run_datetime, rec_datetime): 

		cursor = self.connection.cursor()

		query = "INSERT INTO [{0}] (Run_DateTime, Prediction_DateTime) VALUES('{1}', '{2}')"
		query = query.format(table, str(run_datetime)[:19], str(rec_datetime)[:19])	
		cursor.execute(query)

		cursor.commit()
		cursor.close()


	def __del__(self):
		self.connection.close()

