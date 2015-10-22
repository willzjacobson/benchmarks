#!/bin/env python


import datetime
from collections import OrderedDict


def get_raw_weather_data(cursr, database, table, forecast_table,
		forecast_start_ts, options, lgr):

	""" get raw weather data from database
		cursr: pre-connected database cursor
		database: name of the database
		table: name of the table containing observed weather data
		forecast_table: name of the table containing forecasted weather data
		forecast_start_ts: forecast start datetime object. This determines
			the time as of which the observed weather data is trucated and
			the most recent forecast available at the time is used
	"""

	# no timestamp specified, use as much observed data as available
	if not forecast_start_ts:
		forecast_start_ts = datetime.datetime(2099, 1, 1)

	query = """
		SELECT * FROM (
			SELECT [%s].dbo.HUMIDEX(Temp, Dewp) humidex, Date
				FROM [%s].[dbo].[%s]
				WHERE Date <= ? 
				AND TEMP > -900 AND Dewp > -900
			UNION
			SELECT [%s].dbo.HUMIDEX(Temp, Dewp) humidex, Date
				FROM [%s].[dbo].[%s]
				WHERE Fcst_Date = (SELECT MAX(Fcst_Date)
									FROM [%s].[dbo].[%s]
									WHERE Fcst_Date <= ?)
				AND Date >= ?
				AND TEMP > -900 AND Dewp > -900) t
		ORDER BY Date
	""" % (database, database, table, database, database, forecast_table,
		database, forecast_table)

	if options.debug is not None and options.debug == 1:
		lgr.info('fetching weather: %s, %s' % (query, forecast_start_ts))

	cursr.execute(query, forecast_start_ts, forecast_start_ts, forecast_start_ts)
	weather_data = OrderedDict([])

	for row in cursr.fetchall():
		humidex, edt_ts = row[0], datetime.datetime.strptime(
			str(row[1]).encode('utf8')[:-8], '%Y-%m-%d %H:%M:%S')
		weather_data[edt_ts] = humidex

	return weather_data

