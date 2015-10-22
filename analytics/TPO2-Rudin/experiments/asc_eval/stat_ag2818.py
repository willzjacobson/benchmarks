""" 
Report Thermal ASC performance
"""

from nert import *
import datetime as dt
import numpy
import math
from array import *

import optparse
import cfgparse

import datetime
from common_rudin.common import log_from_config, setup, setup_cparser
import common_rudin.utils as utils
import common_rudin.db_utils as db_utils

_module = 'asc_stat'

#bms_server = "anderson.ldeo.columbia.edu"
#bms_database = "345"
#bms_user = "Hooshmand"
#bms_pwd = "Breakit68"

STEAM_PENALTY_BEGIN_HOUR = 6
# ag2818: do not compute preheat time when the penalty not in effect

#_from_dt = dt.datetime(2014, 12, 28)
#_to_dt = dt.datetime(2015, 1, 13)
ONE_DAY = dt.timedelta(days=1)


# group name: table, discrete, domain, control;
#fan_table = '345---------001BMSHVAFANLCP---VAL001'
pum_table = '345---------001BMSWATSECPUM---VAL001'
#tem_table = '345---------001BMSHVATEMSPA---VAL001'
#ele_table = '345---------001BMSELEMET------VAL001'
#ste_table = '345---------001BMSSTEMET------VAL001'
#occ_table = '345---------000SECCNTPEOBUI---VAL001'

#Floors = 'F02, F04, F04, F05, F13, F18, F20, F24, F32, F38, F40'
#Quadrants= 'CNW, CNW, CSE, CSE, CSW, CSE, CSW, CSE, CNW, CNW, CNE'


fan_out_table = '345---------001TPOHVAFANLCP---VAL001'
pum_out_table = '345---------001TPOWATSECPUM---VAL001'
tem_out_table = 'asc_output_temp'
ele_out_table = 'asc_output_electric'
ste_out_table = 'asc_output_steam'
occ_out_table = 'asc_output_occupancy'

# def startup_preheat(df):
	# f = numpy.array([df.X.T[i] for i in df.group['fan']])
	# p = numpy.array([df.X.T[i] for i in df.group['pump']])

	# S = f[0]
	# for i in range(1, len(f)):
		# S += f[i]
	# P = p[0]
	# for i in range(1, len(f)):
		# P += f[i]


	# AS = []
	# AP = []


def save_cost_data(cnxn, cost_data, options, lgr):
	""" save cost comparison data to db """

	# if data for a date already exists, insert should fail;
	# update will be attempted in this case
	# A small number of rows (mostly like only 1) are
	# expected to be inserted every day so we can do this one row at a time
	# without taking a performance hit
	insert_stmt = """
		INSERT INTO [%s].dbo.[%s]
		(Cost_date, Actual_cost, Predicted_cost) VALUES (?, ?, ?)
	""" % (options.results_db, 'Thermal_ASC_Perf_Cost')
	update_stmt = """
		UPDATE [%s].dbo.[%s]
		SET Actual_cost = ?, Predicted_cost = ?
		WHERE Cost_date = ?
	""" % (options.results_db, 'Thermal_ASC_Perf_Cost')
	
	# save data to table
	crsr = cnxn.cursor()
	for data in cost_data:
		dt, adf, pdf = data
		try:
			crsr.execute(insert_stmt, (dt, adf, pdf))
		except Exception, e: # insert failed, try updating
			lgr.info(e)
			try:
				crsr.execute(update_stmt, (adf, pdf, dt))
			except Exception, e: # something went wrong
				lgr.critical('error saving cost data: %s' % e)
				raise e

	# all OK
	cnxn.commit()


def save_startup_preheat_data(cnxn, perf_data, options, lgr):
	""" save startup and preheat ASC vs actual data to db """
	
	# if data for a date already exists, insert should fail;
	# update will be attempted in this case
	# A small number of rows (mostly like only 1) are
	# expected to be inserted every day so we can do this one row at a time
	# without taking a performance hit
	insert_stmt = """
		INSERT INTO [%s].dbo.[%s]
		(Perf_date, Actual_startup, Recommended_startup, Actual_preheat_tm,
			Recommended_preheat_tm) VALUES (?, ?, ?, ?, ?)
	""" % (options.results_db, 'Thermal_ASC_Perf')
	update_stmt = """
		UPDATE [%s].dbo.[%s]
		SET Actual_startup = ?, Recommended_startup = ?, Actual_preheat_tm = ?,
			Recommended_preheat_tm = ?
		WHERE Perf_date = ?
	""" % (options.results_db, 'Thermal_ASC_Perf')

	# save data to table
	crsr = cnxn.cursor()
	for data in perf_data:
		dt, adf_preheat, pdf_preheat, adf_startup, pdf_startup = data
		
		# check for missing values; if a value is missing, set it to NULL in db
		upd_tms = []
		for tm in [adf_preheat, pdf_preheat, adf_startup, pdf_startup]:
			if 'no' in tm:
				lgr.info(tm)
				upd_tms.append(None)
			else:
				upd_tms.append(tm)

		adf_preheat, pdf_preheat, adf_startup, pdf_startup = upd_tms
		
		try:
			#qry = insert_stmt.format(dt, adf_startup, pdf_startup,
			#	adf_preheat, pdf_preheat)
			#lgr.info(qry)
			crsr.execute(insert_stmt, (dt, adf_startup, pdf_startup,
				adf_preheat, pdf_preheat))
		except Exception, e: # insert failed, try updating
			lgr.info(e)
			try:
				crsr.execute(update_stmt, (adf_startup, pdf_startup,
					adf_preheat, pdf_preheat, dt))
			except Exception, e: # something went wrong
				lgr.critical('error saving cost data: %s' % e)
				raise e

	# all OK
	cnxn.commit()


# logging support
version = "%prog 0.1"
usage = "usage: %prog [options]"

oparser = optparse.OptionParser(usage=usage, version=version,
		description=__doc__)
cparser = cfgparse.ConfigParser()
setup(oparser, cparser, _module)

# read configuration file
options, args = cparser.parse(oparser, None)

lgr = log_from_config(options, _module)
lgr.info('*** %s starting up' % _module)

arg_count = len(args)

run_ts = datetime.datetime.now()
lgr.info('run time: %s, %d' % (run_ts, arg_count))

# if no argument, compute results for previous day
as_of_dt = None
if arg_count == 0:
	as_of_dt = datetime.datetime.combine(run_ts.date() - ONE_DAY,
		datetime.time(0, 0, 0))

# if a date is specified, 
elif arg_count == 3:
	int_args = map(int, args)
	as_of_dt = datetime.datetime(int_args[0], int_args[1], int_args[2])
else:
	lgr.critical(args)
	oparser.error("incorrect number of arguments")

#_from_dt = dt.datetime(2015, 1, 13)
#_to_dt = dt.datetime(2015, 2, 2)#dt.datetime(2014, 03, 01)
_to_dt = as_of_dt
_from_dt = _to_dt - 2*ONE_DAY

lgr.info('from_dt: %s, to_dt: %s' % (_from_dt, _to_dt))

_to = str(_to_dt)[:19]
_from = str(_from_dt)[:10]

	
# Floors = Floors.replace(' ', '').split(',')
# Quadrants = Quadrants.replace(' ', '').split(',')

## loop over buildings in the config file
# get building ids
building_ids = utils.parse_value_list(options.building_ids)

reinstantiate_cparser = False
for bldg_idx, building_id in enumerate(building_ids):

	if bldg_idx != 0:
		reinstantiate_cparser = True
	options = utils.load_bldg_config(building_id, oparser, cparser, None,
		options, lgr, reinstantiate_cparser)

	if '345' not in building_id:
		lgr.info('skipping bldg. %s' % building_id)
		continue
	
	bldg_floors, floor_quadrants, _, _ = utils.get_floors_quadrants(
														options, lgr)

	#temp_keys = zip(tuple(Floors), tuple(Quadrants))
	temp_keys = zip(tuple(bldg_floors), tuple(floor_quadrants))
	
	### FOR ACTUAL DATA

	#bms_interface = DatabaseInterface(bms_server, bms_database, bms_user, bms_pwd)
	bms_interface = DatabaseInterface(options.building_db_server,
		options.building_db, options.db_user, options.db_pwd)
	s = []
	# Actions
	s += bms_interface.get_bms_series(options.fan_table, _from, _to, _group='fan', _discrete=True)
	s += bms_interface.get_bms_series(pum_table, _from, _to, _group='pump', _discrete=True)

	# States
	s += bms_interface.get_bms_series(options.space_temp_tablename_format,
		_from, _to, _keys=temp_keys, _group='temp', _domain=(0, 120))

	s += bms_interface.get_bms_series(options.electric_load_table, _from, _to,
		_group='electric', _domain=(0, 1500))
	s += bms_interface.get_bms_series(options.steam_demand_table, _from, _to,
		_group='steam')
	s += bms_interface.get_bms_series(options.occupancy_table, _from, _to,
		_group='occupancy')

	#adf is the DataFrame for the actual data
	adf = DataFrame()  
	adf.add_series(s)
	if options.debug:
		adf.plot()

	#Initializing variables 
	today = _from_dt #dt.datetime(2014, 1, 15) #start date for the evaluation period
	lgr.info('%s, %s' % (today, _from))
	tomorrow = today + dt.timedelta(1)
	adf_cost = []
	adf_startup = []
	adf_preheat = []
	lgr.info('building open hour: %d' % options.building_open_hour)
	while today <= _to_dt - ONE_DAY: #dt.datetime(2014, 2, 28):
		if (today.weekday() >=5): #avoid weekends
			today += dt.timedelta(1)
			tomorrow += dt.timedelta(1)
			continue
			
		#getting one day subset of the DataFrame
		temp_df = adf.subset(today, tomorrow)  
		lgr.info('today: %s, tomm: %s' % (today, tomorrow))
		#Startup time calculation
		fans = ([temp_df.X.T[i] for i in temp_df.group['fan']])
		fan_od = [] #fan_od stores values for all fans for the startup time period (4 AM to 7 AM) (for debudding purposes)
		earliest_on = float("inf")
		for fan_no in range(0, len(fans)):
			fan_od.append([])
			for point in range(1, len(fans[fan_no])):
				hour = int(temp_df.timestamps[point].strftime("%H"))
				minute = int(temp_df.timestamps[point].strftime("%M"))
				if ((hour >= 04 and hour < options.building_open_hour)
						or (hour == options.building_open_hour and minute == 00)):
					fan_od[fan_no].append(fans[fan_no][point])
				if ((fans[fan_no][point] == 1.0 and fans[fan_no][point-1] == 0.0)
						and ((hour >= 04 and hour < options.building_open_hour)
								or (hour == options.building_open_hour and minute == 00))) :
					if (point <= earliest_on): #storing the time for the earliest change from 0 to 1 for any of the fans
						earliest_on = point
						
		if (earliest_on == float("inf")):
			adf_startup.append('no startup')
			val = 'no startup'
		else:
			adf_startup.append(temp_df.timestamps[earliest_on].strftime("%H:%M:%S"))
			val = temp_df.timestamps[earliest_on].strftime("%H:%M:%S")
			
		#displaying fan_od data for debugging (checking if the earliest_on time was correct)
		"""
		print 'ACTUAL FANS FOR'
		print (today.isoformat() + " to " +tomorrow.isoformat())
		print 'Time starts at 4 AM'
		for i in range(0, len(fans)):
			print fan_od[i]
		s = 'Startup Time: '+val
		print s
		"""
		
		#WORK FOR PUMPS ---- ABANDONED BECAUSE PUMP DATA WAS NOT ENOUGH FOR COMPUTING PREHEAT TIME
		"""
		pumps = ([temp_df.X.T[i] for i in temp_df.group['pump']])
		pump_od=[]
		earliest_on = float("inf")
		for pump_no in range(0, len(pumps)):
			pump_od.append([])
			for point in range(1, len(pumps[pump_no])):
				hour = int(temp_df.timestamps[point].strftime("%H"))
				minute = int(temp_df.timestamps[point].strftime("%M"))
				if ((hour >= 02 and hour < 07) or (hour == 07 and minute == 00)):
					pump_od[pump_no].append(pumps[pump_no][point])
				if (pumps[pump_no][point] == 1.0 and pumps[pump_no][point-1] == 0.0) and ((hour >= 02 and hour < 07) or (hour == 07 and minute == 00)) :
					if (point <= earliest_on):
						earliest_on = point
		if (earliest_on == float("inf")):
			adf_preheat.append('no preheat')
			val = 'no preheat'
		else:
			adf_preheat.append(temp_df.timestamps[earliest_on].strftime("%H : %M : %S"))
			val = temp_df.timestamps[earliest_on].strftime("%H : %M : %S")
		
		print ' '
		print 'ACTUAL PUMPS FOR'
		print (today.isoformat() + " to " +tomorrow.isoformat())
		print 'Time starts at 2 AM'
		for i in range(0, len(pumps)):
			print pump_od[i]
		s = 'Preheat Time: '+val
		print s
		print ' '"""
		
		
		#Preheat time calculation
		steam = ([temp_df.X.T[i] for i in temp_df.group['steam']])
		max_val = 0 #the maximum value in the steam series is to be stored in max_val because this represents the preheat peak
		max_val_time = 0
		steam_od = [] #for debugging purposes

		if run_ts.month > 11 or run_ts.month < 4: # ag2818: preheat only in winter
			for point in range(1, len(steam[0])):
				hour = int(temp_df.timestamps[point].strftime("%H"))
				minute = int(temp_df.timestamps[point].strftime("%M"))
				if ((hour >= 02 and hour < STEAM_PENALTY_BEGIN_HOUR)
						or (hour == STEAM_PENALTY_BEGIN_HOUR and minute == 00)):
					steam_od.append(steam[0][point])
				if ((steam[0][point] > max_val)
						and ((hour >= 02 and hour < STEAM_PENALTY_BEGIN_HOUR)
								or (hour == STEAM_PENALTY_BEGIN_HOUR and minute == 00))):
					max_val = steam[0][point]
					max_val_time = point
		
		#output for debugging purposes
		"""
		print 'ACTUAL STEAM DATA'
		print 'Time starts at 2 AM'
		print steam_od
		s = 'Preheat Time: '+val
		print s
		print ' '
		"""
		
		if (max_val < 15): #15 was chosen as the preheat peak threshold based on observation from graphs for different days
			adf_preheat.append('no preheat')
			val = 'no preheat'
		else: #if preheat peak is seen, the time for preheat is set to 15 minutes before the peak
			adf_preheat.append(temp_df.timestamps[max_val_time - 1].strftime("%H:%M:%S"))
			val = temp_df.timestamps[max_val_time - 1].strftime("%H:%M:%S")
		
		#Cost calculations
		adf_cost.append(cost(temp_df, factorize=True)[3])
		
		#updating variables for loop
		today += dt.timedelta(1)
		tomorrow += dt.timedelta(1)


	### FOR ASC RECOMMENDATIONS
		
	s = []
	s += bms_interface.get_bms_series(fan_out_table, _from, _to, _group='fan', _discrete=True)
	s += bms_interface.get_bms_series(pum_out_table, _from, _to, _group='pump', _discrete=True)

	# States
	# s += bms_interface.get_bms_series(tem_out_table, _from, _to, _keys=temp_keys, _group='temp', _domain=(0, 120))

	# s += bms_interface.get_bms_series(ele_out_table, _from, _to, _group='electric', _domain=(0, 1500))
	# s += bms_interface.get_bms_series(ste_out_table, _from, _to, _group='steam')
	# s += bms_interface.get_bms_series(occ_out_table, _from, _to, _group='occupancy')
	s += bms_interface.get_overlapping_series(tem_out_table, _from, _to,
		_keys=temp_keys, _group='temp', _domain=(0, 120))

	s += bms_interface.get_overlapping_series(ele_out_table, _from, _to,
		_group='electric', _domain=(0, 1500))
	s += bms_interface.get_overlapping_series(ste_out_table, _from, _to,
		_group='steam')
	s += bms_interface.get_overlapping_series(occ_out_table, _from, _to,
		_group='occupancy')

	pdf = DataFrame()
	pdf.add_series(s)
	if options.debug:
		pdf.plot()


	today = _from_dt #dt.datetime(2014, 1, 15)
	tomorrow = today + dt.timedelta(1)
	pdf_cost = []
	from_date = []
	to_date = []
	pdf_startup = []
	pdf_preheat = []

	fan_data = []
	point_data = []

	while today <= _to_dt - ONE_DAY: #dt.datetime(2014, 2, 28):
		if (today.weekday() >=5): #skipping weekends
			today += dt.timedelta(1)
			tomorrow += dt.timedelta(1)
			continue
		
		lgr.info('today: %s' % today)
		try:
			temp_df = pdf.subset(today, tomorrow) #getting one day subset of the DataFrame
		except Exception, e:
			lgr.info('An unknown error occurred: %s' % e)
			today += ONE_DAY
			tomorrow += ONE_DAY
			continue
		
		#Startup time calculation for recommendations - Same as for actual data
		fans = ([temp_df.X.T[i] for i in temp_df.group['fan']])
		fan_od = []
		no_of_fans = len(fans)
		earliest_on = float("inf")
		
		for fan_no in range(0, len(fans)):
			fan_od.append([])
			for point in range(1, len(fans[fan_no])):
				hour = int(temp_df.timestamps[point].strftime("%H"))
				minute = int(temp_df.timestamps[point].strftime("%M"))
				if ((hour >= 04 and hour < options.building_open_hour)
						or (hour == options.building_open_hour and minute == 00)):
					fan_od[fan_no].append(fans[fan_no][point])
				if ((fans[fan_no][point] == 1.0 and fans[fan_no][point-1] == 0.0)
						and ((hour >= 04 and hour < options.building_open_hour)
								or (hour == options.building_open_hour and minute == 00))):
					if (point <= earliest_on):
						earliest_on = point

		#debugging section
		"""
		print 'RECOMMENDED FANS FOR'
		print (today.isoformat() + " to " +tomorrow.isoformat())
		print 'Time starts at 4 AM'
		for i in range(0, len(fans)):
			print fan_od[i]
		s = 'Startup Time: ' + val
		print s
		"""
		
		if (earliest_on == float("inf")):
			pdf_startup.append('no startup')
			val = 'no startup'
		else:
			pdf_startup.append(temp_df.timestamps[earliest_on].strftime("%H:%M:%S"))
			val = temp_df.timestamps[earliest_on].strftime("%H:%M:%S")
		
		
		#WORK FOR PUMPS ---- ABANDONED BECAUSE PUMP DATA WAS NOT ENOUGH FOR COMPUTING PREHEAT TIME
		"""
		pumps = ([temp_df.X.T[i] for i in temp_df.group['pump']])
		pump_od = []
		earliest_on = float("inf")
		for pump_no in range(0, len(pumps)):
			pump_od.append([])
			for point in range(1, len(pumps[pump_no])):
				hour = int(temp_df.timestamps[point].strftime("%H"))
				minute = int(temp_df.timestamps[point].strftime("%M"))
				if ((hour >= 02 and hour < 07) or (hour == 07 and minute == 00)):
					pump_od[pump_no].append(pumps[pump_no][point])
				if (pumps[pump_no][point] == 1.0 and pumps[pump_no][point-1] == 0.0) and ((hour >= 02 and hour < 07) or (hour == 07 and minute == 00)) :
					if (point <= earliest_on):
						earliest_on = point
		if (earliest_on == float("inf")):
			pdf_preheat.append('no preheat')
			val = 'no preheat'
		else:
			pdf_preheat.append(temp_df.timestamps[earliest_on].strftime("%H : %M : %S"))
			val = temp_df.timestamps[earliest_on].strftime("%H : %M : %S")
		
		print ' '
		print 'RECOMMENDED PUMPS FOR'
		print (today.isoformat() + " to " +tomorrow.isoformat())
		print 'Time starts at 2 AM'
		for i in range(0, len(pumps)):
			print pump_od[i]
		s = 'Preheat Time: ' + val
		print s
		print ' '
		"""
		
		#Preheat time calculation - Same as for actual data
		steam = ([temp_df.X.T[i] for i in temp_df.group['steam']])
		max_val = 0
		max_val_time = 0
		steam_od = []
		
		if run_ts.month > 11 or run_ts.month < 4: # ag2818: preheat only in winter
			for point in range(1, len(steam[0])):
				hour = int(temp_df.timestamps[point].strftime("%H"))
				minute = int(temp_df.timestamps[point].strftime("%M"))
				if ((hour >= 02 and hour < STEAM_PENALTY_BEGIN_HOUR)
						or (hour == STEAM_PENALTY_BEGIN_HOUR and minute == 00)) :
					steam_od.append(steam[0][point])
				if ((steam[0][point] > max_val)
						and ((hour >= 02 and hour < STEAM_PENALTY_BEGIN_HOUR)
								or (hour == STEAM_PENALTY_BEGIN_HOUR and minute == 00))):
					max_val = steam[0][point]
					max_val_time = point
				
		
		#debugging section
		"""
		print 'RECOMMENDED STEAM DATA'
		print 'Time starts at 2 AM'
		print steam_od
		s = 'Preheat Time: '+val
		print s
		print ' '
		"""
		
		if (max_val < 15):
			pdf_preheat.append('no preheat')
			val = 'no preheat'
		else:
			pdf_preheat.append(temp_df.timestamps[max_val_time - 1].strftime("%H:%M:%S"))
			val = temp_df.timestamps[max_val_time - 1].strftime("%H:%M:%S")
		

		#storing dates for CSV
		from_date.append(today.strftime("%m-%d-%Y")) 
		to_date.append(tomorrow.isoformat())
		
		pdf_cost.append(cost(temp_df, factorize=True)[3])
		today += dt.timedelta(1)
		tomorrow += dt.timedelta(1)

	#GENERATING CSVs

	adf_cost_n = numpy.asarray(adf_cost)
	pdf_cost_n = numpy.asarray(pdf_cost)
	#cost_eval = numpy.vstack((from_date, to_date, adf_cost_n, pdf_cost_n))
	cost_eval = numpy.vstack((from_date, adf_cost_n, pdf_cost_n))
	cost_eval = numpy.transpose(cost_eval)
	numpy.savetxt("cost_eval.csv", cost_eval, delimiter=",", fmt="%s")
	
	# TODO: save to database
	results_db_conn, _ = db_utils.connect(options.db_driver,
		options.results_db_user, options.results_db_pwd,
		options.results_db, options.results_db_server)

	save_cost_data(results_db_conn, cost_eval, options, lgr)

	adf_preheat_n = numpy.asarray(adf_preheat)
	pdf_preheat_n = numpy.asarray(pdf_preheat)
	adf_startup_n = numpy.asarray(adf_startup)
	pdf_startup_n = numpy.asarray(pdf_startup)
	startup_preheat = numpy.vstack((from_date, adf_preheat, pdf_preheat, adf_startup, pdf_startup))
	#startup_preheat = numpy.vstack((from_date, adf_startup, pdf_startup))
	startup_preheat = numpy.transpose(startup_preheat)
	numpy.savetxt("startup_preheat.csv", startup_preheat, delimiter=",", fmt="%s")
	
	# save data
	save_startup_preheat_data(results_db_conn, startup_preheat, options, lgr)


