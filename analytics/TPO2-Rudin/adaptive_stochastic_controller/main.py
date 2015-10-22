
import sys
import optparse
from optparse import OptionParser
import ConfigParser

from common_rudin.common import log_from_config, setup, setup_cparser
import common_rudin.utils as utils

import pyodbc

import datetime as dt

import numpy

import pickle

import traceback

import DatabaseInterface as dbi
import DataFrame as DF
import ResponseModel as rm
import Optimization as opt

_module = 'asc'

#def search(_from, _to):
def search(argv):

	parser = OptionParser()
	parser.add_option("-b", "--building", dest="section", help="Building section in config file", metavar="BUILDING")
	parser.add_option("-f", "--from", dest="from", help="Building section", metavar="FROM")
	parser.add_option("-c", "--config", dest="config", help="Configuration File", metavar="CONFIG")
	parser.add_option("-z", "--horizon", dest="horizon", help="Horizon of forecast and optimization", metavar="HORIZON")
	parser.add_option("-w", "--window", dest="window", help="Window of history", metavar="WINDOW")


	(options, args) = parser.parse_args()

	print "Running ASC for " + options.section

	now = str(dt.datetime.now())[:19]

	if options.config == None:
		cfile = './config.ini'
	else:
		cfile = options.config

	#cfile = options.config
	#section = 'Rudin_345Park'
	section = options.section

	cparser = ConfigParser.ConfigParser()
	cparser.readfp(open(cfile))	

	#################################
	#return	
	#_to = dt.datetime.now()

	#window of history in days;
	#default is set to 30 days
	if options.window == None:
		days_before = 30
	else:	
		days_before = int(options.window)

	#default horizon is set to 24 hours
	try:
		horizon = int(options.horizon)
	except:
		horizon = 24
	print "Horizon set at {0} hours".format(horizon)

	if horizon > 36:
		print "Horizon greater that 36 hours is not recommended!"
	
	#run as of the date specified by _to
	#_to is set to system clock current time
	_to = dt.datetime.now()
	_from = _to - dt.timedelta(days_before )

	_to = str(_to)[:19]
	_from = str(_from)[:10]


	bms_server = cparser.get(section, 'building_db_server')
	bms_database = cparser.get(section, 'building_db')
	bms_user = cparser.get(section, 'db_user')
	bms_pwd = cparser.get(section, 'db_pwd')


	has_steam = cparser.getint(section, 'has_steam_supply')

	if has_steam:
		print "{0} has steam.".format(options.section)
	else:
		print "{0} has NO steam.".format(options.section)

	weather_section = cparser.get(section, 'weather_station_id')

	weather_server = cparser.get(weather_section, 'weather_db_server')
	weather_database = cparser.get(weather_section, 'weather_db')
	weather_user = cparser.get(weather_section, 'weather_db_user')
	weather_pwd = cparser.get(weather_section, 'weather_db_pwd')

	weather_table = cparser.get(weather_section, 'weather_table')
	weather_fcst_table = cparser.get(weather_section, 'weather_forecast_table')

	tpo_server = cparser.get(section, 'results_db_server')
	tpo_database = cparser.get(section, 'results_db')
	tpo_user = cparser.get(section, 'results_db_user')
	tpo_pwd = cparser.get(section, 'results_db_pwd')

	# group name: table, discrete, domain, control;
	fan_table = cparser.get(section, 'fan_table')
	vfd_table = cparser.get(section, 'vfd_table')
	if has_steam:
		pum_table = cparser.get(section, 'pump_table')
		wsp_table = cparser.get(section, 'water_set_point_table')
	tem_table = cparser.get(section, 'space_temp_tablename_format')
	ele_table = cparser.get(section, 'electric_load_table_orig')
	if has_steam:
		ste_table = cparser.get(section, 'steam_demand_table')
	occ_table = cparser.get(section, 'occupancy_table')


	Floors = cparser.get(section, 'building_floors')
	Quadrants = cparser.get(section, 'floor_quadrants')


	output_table = {}
	#the following options have to be manually added to the configuration file
	output_table['startup'] = cparser.get(section, 'results_table_startup')
	output_table['fan'] = cparser.get(section, 'asc_output_fan_table')
	output_table['vfd'] = cparser.get(section, 'asc_output_vfd_table')
	if has_steam:
		output_table['wsp'] = cparser.get(section, 'asc_output_sec_table') 
		output_table['pump'] = cparser.get(section, 'asc_output_pump_table')
	output_table['electric'] =  cparser.get(section, 'asc_output_electric_table')
	if has_steam:
		output_table['steam'] = cparser.get(section, 'asc_output_steam_table') 
	output_table['occupancy'] = cparser.get(section, 'asc_output_occupancy_table')
	output_table['temp'] = cparser.get(section, 'asc_output_temp_table')

	'''
	output_table['fan'] = '345---------001TPOHVAFANLCP---VAL001'
	output_table['vfd'] = '345---------001TPOHVAFANFDB---VAL001'
	if has_steam:
		output_table['wsp'] = '345---------001TPOWATSEC------VAL001'
		output_table['pump'] = '345---------001TPOWATSECPUM---VAL001'
	output_table['electric'] = 'asc_electric_output_electric'
	if has_steam:
		output_table['steam'] = 'asc_electric_output_steam'
	output_table['occupancy'] = 'asc_electric_output_occupancy'
	output_table['temp'] = 'asc_electric_output_temp'
	'''


	Floors = Floors.replace(' ', '').split(',')
	Quadrants = Quadrants.replace(' ', '').split(',')

	temp_keys = zip(tuple(Floors), tuple(Quadrants))

	################################################

	bms_interface = dbi.DatabaseInterface(bms_server, bms_database, bms_user, bms_pwd)
	tpo_interface = dbi.DatabaseInterface(tpo_server, tpo_database, tpo_user, tpo_pwd)

	s = []
	# Actions
	s += bms_interface.get_bms_series(fan_table, _from, _to, _group='fan', _discrete=True)
	s += bms_interface.get_bms_series(vfd_table, _from, _to, _group='vfd')
	if has_steam:
		s += bms_interface.get_bms_series(pum_table, _from, _to, _group='pump', _discrete=True)
		s += bms_interface.get_bms_series(wsp_table, _from, _to, _group='wsp')

	# States
	s += bms_interface.get_bms_series(tem_table, _from, _to, _keys=temp_keys, _group='temp', _domain=(0, 120))
	s += bms_interface.get_bms_series(ele_table, _from, _to, _group='electric', _domain=(0, 1500))
	if has_steam:
		s += bms_interface.get_bms_series(ste_table, _from, _to, _group='steam')
	s += bms_interface.get_bms_series(occ_table, _from, _to, _group='occupancy')

	weather_interface = dbi.DatabaseInterface(weather_server, weather_database, weather_user, weather_pwd)
	s += weather_interface.get_generic_series((weather_table, "Weather"), "Date", [("TempA", "Temp"), ("DewPointA", "DewPoint"), ("Humidity", "Humidity")], _from, _to, _group='weather')

	df = DF.DataFrame()
	df.add_series(s)

	#df.refine("occupancy", ["weather", "time"])

	df.gaps()
	gaps = df.data_gaps

	mrt = rm.MarkovRandomizedTree(df)	
	mrt.addDependency('time', 'time')
	mrt.addDependency('occupancy', ['occupancy', 'time', 'weather'])
	mrt.addDependency('electric', ['electric', 'occupancy', 'fan', 'vfd'])
	if has_steam:
		mrt.addDependency('steam', ['steam', 'pump', 'wsp'])
	if has_steam:
		mrt.addDependency('temp', ['temp', 'weather', 'fan', 'pump', 'steam', 'wsp', 'vfd'])
	else:
		mrt.addDependency('temp', ['temp', 'weather', 'fan', 'vfd'])
	mrt.addDependency('weather', ['weather', 'time'])


	form = "%Y-%m-%d"
	_from = dt.datetime.strptime(_from, form)
	_to = dt.datetime.strptime(_to, form+" %H:%M:%S")

	##################################################

	print "Retrieving weather forecast data..."

	ndf = df.subset(_from, _to)
	_before = str(_to + dt.timedelta(horizon/24, horizon%24))[:19]
	t = weather_interface.get_forecast_series((weather_fcst_table, "Weather"), "Fcst_date", "Date", [("TempA", "Temp"), ("DewA", "DewPoint"), ("Humidity", "Humidity")], _to, _before, _group='weather')

	print "Retrieving lastest states of actions..."

	t += bms_interface.get_bms_series(fan_table, _from, _to, _group='fan', _discrete=True, last=True)
	t += bms_interface.get_bms_series(vfd_table, _from, _to, _group='vfd', last=True)
	if has_steam:
		t += bms_interface.get_bms_series(pum_table, _from, _to, _group='pump', _discrete=True, last=True)
		t += bms_interface.get_bms_series(wsp_table, _from, _to, _group='wsp', last=True)


	odf = DF.DataFrame()
	odf.add_series(t)


	mrt.fit()
	bestDF = opt.search(df, odf, mrt)

	startup_datetime = opt.startup(bestDF)
	tpo_interface.commit_recommendation(output_table['startup'], now, str(startup_datetime)[:19])
	#print opt.preheat(bestDF)
	
	for g in ['vfd', 'electric', 'temp', 'occupancy']:

		for i in bestDF.group[g]:
			print "Commiting to " + output_table[g] + "..."
			tpo_interface.commit_bms_series(output_table[g], now, bestDF.pointnames[i], bestDF.timestamps, bestDF.X.T[i])
			print "Sucessful!"


	if has_steam:
		for g in ['steam', 'pump']:
		#for g in ['steam', 'wsp', 'pump']:

			for i in bestDF.group[g]:
				print "Commiting to " + output_table[g] + "..."
				tpo_interface.commit_bms_series(output_table[g], now, bestDF.pointnames[i], bestDF.timestamps, bestDF.X.T[i])
				print "Sucessful!"



if __name__ == '__main__':

	search(sys.argv)


