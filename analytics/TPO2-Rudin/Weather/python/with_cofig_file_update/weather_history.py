__author__ = 'vanamali'

# This retrieves the observation history.
# for DEVELOPER License We have 500 calls per day at a max rate of 10 calls per minute
# DEVELOPER License is free.
_module = 'History_NY_KNYC' #edit

import os
import sys
import urllib2
import json
import datetime
import time
import pyodbc
import optparse
import cfgparse
from common import setup, log_from_config # edit

#if argv is None:
argv = sys.argv

version = "%prog 0.2"
usage = "usage: %prog [options]"
  
parser = optparse.OptionParser(usage=usage, version=version, description=__doc__)
cparser = cfgparse.ConfigParser()
setup(parser, cparser, _module)

mod_optgroup = parser.add_option_group('%s Options' % _module)
mod_cfggroup = cparser.add_option_group('%s Options' % _module)

# here is where options are added
mod_optgroup.add_option("--driver", 
      help="db driver name")
mod_cfggroup.add_option('driver', keys=_module)

mod_optgroup.add_option("--server", 
      help="db server name")
mod_cfggroup.add_option('server', keys=_module)

mod_optgroup.add_option("--database", 
      help="db database name,   ")
mod_cfggroup.add_option('database', keys=_module)

mod_optgroup.add_option("--UID", 
      help="db user name,   ")
mod_cfggroup.add_option('UID', keys=_module)

mod_optgroup.add_option("--PWD", 
      help="db user password,   ")
mod_cfggroup.add_option('PWD', keys=_module)

mod_optgroup.add_option("--table", 
      help="db table name,   ")
mod_cfggroup.add_option('table', keys=_module)

mod_optgroup.add_option("--api_key", 
      help="API key, get one from http://api.wunderground.com/api")
mod_cfggroup.add_option('api_key', keys=_module)

mod_optgroup.add_option("--location", 
      help="location use  NY/New_York or KNYC for Central Park, KLGA is LaGuardia, pws:KNYBROOK40 is a Williamsburg, for example, personal station ")
mod_cfggroup.add_option('location', keys=_module)

mod_optgroup.add_option("--delta", type="int",
      help="how many days to truncate before adding WX data to the DB")
mod_cfggroup.add_option('delta', keys=_module)

mod_optgroup.add_option("--start", 
      help="Date (YYYY-MM-DD) to start populating the weather history. If the value is latest, will start from latest date in existing table")
mod_cfggroup.add_option('start', keys=_module)

(options, args) = cparser.parse(parser, argv)
#lgr.debug('opening my_netrms with %s' % options.netrms_db)
#lgr.debug(par) 

Driver = options.driver
Server = options.server
Database = options.database
UID = options.UID
PWD = options.PWD
table = options.table
api_key = options.api_key
location = options.location
delta_days = options.delta
start_date = options.start

CONNECTION_STRING ="""
Driver=%s;
Server=%s;
Database=%s;
UID=%s;
PWD=%s;
Trusted_Connection=No;
""" % (Driver, Server, Database, UID, PWD)

connection = pyodbc.connect(CONNECTION_STRING)
c = connection.cursor()
'''
#test connection
print CONNECTION_STRING
query ="select COUNT(*) from Observations_History"
c.execute(query)
for row in c.fetchall():
	print row[0]
'''

#Processing data to fit the query
delta = datetime.timedelta(days=delta_days)
today = datetime.datetime.today()

#cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

#start at 4AM -- No longer use local time now (was 4 below)
if start_date == 'latest':
    query = "select max(Date) as max_date FROM [dbo].%s" % (table)
    try: 
        c.execute(query)
        row = c.fetchone()
    except Exception as e:
            #print "Problem deleting data from Weather Obs Table %s" % e
            lgr.error("Attention: Problem querying for max date from Weather Obs Table %s, exiting" % (table))
            raise
    print 'last date in DB is %s' % row[0]
    #print 'delta is: %s' %delta
    #lgr.info('last date in DB is %s' % row[0])
    #last_day = row[0] - delta
    last_day = row[0]
    #last_day = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.0000000') - delta
    last_day = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.0000000')
    #start is one day before since we have 4 hrs of extra data (No longer)
    #lgr.info('start date is %s' % last_day)
    cur_year = last_day.year
    cur_mo   = last_day.month
    cur_day  = last_day.day
    cur_date = datetime.datetime(cur_year,cur_mo,cur_day,0)
else:
    cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
       

#Use this to initialize the table
#cur_date = datetime.datetime(2012,03,30,0)

#lgr.info( 'Deleting from %s' % (cur_date))
#DELETE FROM [dbo].[Weather_raw] WHERE date > '2012-08-15 04:00'
#delete any entries after our start date
query = "DELETE FROM [dbo].%s WHERE [Date] >= ?" % (table)
try:
    c.execute (query, [cur_date])
except Exception as e:
    print "Problem deleting data from Weather Obs Table %s" % e
    #lgr.error("Attention: Problem deleting data from Weather Obs Table %s for date %s" % (table,cur_date))
    raise

# Running the query.    
url = 'http://api.wunderground.com/api/%s/history_%s/q/%s.json'
print "Using this url: %s" % url
#print "Using this url: %s" % url_res
delta_inc = datetime.timedelta(days=1)
d = cur_date
count =0

while d <= today:
    if count<=450:
	url_date = d.strftime("%Y%m%d")
	#lgr.info( 'Getting WX HX for %s' % url_date)
	print 'Getting WX HX for %s' % url_date
	url_res = url % (api_key, url_date, location)
	#lgr.info( "Using this url: %s" % url_res)
	print "Using this url_res: %s" % url_res
	try:
	    f = urllib2.urlopen(url_res)
	    json_string = f.read()
	except Exception as e:
	    #lgr.error("Attention: Error getting data for %s from Weather Underground API: Error %s, skipping day" % (url_date,e))
	    print "Attention: Error getting data for %s from Weather Underground API: Error %s, skipping day" % (url_date,e)
	    continue
	try:
	    parsed_json = json.loads(json_string)
	    odata_list = parsed_json['history']['observations']
	except Exception as e:
	    #lgr.error("Attention: Error parsing jason data for %s from Weather Underground API: Error %s, skipping day" % (url_date,e))
	    print "Attention: Error parsing jason data for %s from Weather Underground API: Error %s, skipping day" % (url_date,e)
	    continue
	for odata in odata_list:
	    try:
		obs_utcmin      = odata['utcdate']['min']
		obs_utchour     = odata['utcdate']['hour']
		obs_utcday      = odata['utcdate']['mday']
		obs_utcmonth    = odata['utcdate']['mon']
		obs_utcyear     = odata['utcdate']['year']
		obs_min         = odata['date']['min']
		obs_hour        = odata['date']['hour']
		obs_day         = odata['date']['mday']
		obs_month       = odata['date']['mon']
		obs_year        = odata['date']['year']

		tempi        = odata['tempi']
		tempm       = odata['tempm']
		
		dewpti       = odata['dewpti']
		dewptm       = odata['dewptm']
		
		hum          =   odata['hum']
		
		wspdi        =   odata['wspdi']
		wspdm        =   odata['wspdm']
		
		wgusti       =   odata['wgusti']
		wgustm       =   odata['wgustm']
		
		wdird        =   odata['wdird']
		#wdire        =   odata['wdire']
		
		visi         =   odata['visi']
		vism         =   odata['vism']
		
		pressurei    =   odata['pressurei']
		pressurem    =   odata['pressurem']

		windchilli   =   odata['windchilli']
		windchillm   =   odata['windchillm']
		
		heatindexi   =   odata['heatindexi']
		heatindexm   =   odata['heatindexm']

		precipi      =   odata['precipi']
		precipm      =   odata['precipm']

		condition    =   odata['conds']
		
		fog          =   odata['fog']
		rain         =   odata['rain']
		snow         =   odata['snow']
		hail         =   odata['hail']
		thunder      =   odata['thunder']
		tornado      =   odata['tornado']

		iso_date    = '%s-%s-%s %s:%s:00' % (obs_year, obs_month, obs_day, obs_hour, obs_min)
		iso_utcdate = '%s-%s-%s %s:%s:00' % (obs_utcyear, obs_utcmonth, obs_utcday, obs_utchour, obs_utcmin)
		#('%Y-%m-%d %H:%M:%S.0000000')
		rec = "%s %s (%s) : %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % (today, iso_date, iso_utcdate, tempi,  dewpti, hum, wspdi, wgusti, wdird, visi,pressurei, windchilli,  heatindexi,precipi, condition, fog, rain, snow, hail, thunder, tornado )
		# print iso_date,  iso_utcdate, tempi,  dewpti, hum, wspdi, wgusti, wdird, visi,pressurei, windchilli,  heatindexi,precipi, condition, fog, rain, snow, hail, thunder, tornado

	    except Exception as e:
		print "Problem parsing obs record %s skipping. Error is %s" %(odata,e)
		#lgr.warning("Problem parsing obs record %s skipping. Error is %s" % (odata,e))
		continue
	    query = "INSERT INTO [dbo].%s ([Run_DateTime], [Date],[UTC_Date],[TempA],[TempM],[DewPointA],[DewPointM],[Humidity],[WindSpeedA],[WindSpeedM],[WindGustA],[WindGustM],[WindDir],[VisibilityA],[VisibilityM],[PressureA],[PressureM],[WindChillA],[WindChillM],[HeatIndexA],[HeatIndexM],[PrecipA],[PrecipM],[Condition],[Fog],[Rain],[Snow],[Hail],[Thunder],[Tornado])  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % table
	    try:
	        c.execute(query, (today, iso_date, iso_utcdate,tempi,tempm,dewpti, dewptm, hum, wspdi,wspdm, wgusti, wgustm,wdird, visi,vism,pressurei,pressurem, windchilli,windchillm,  heatindexi,heatindexm,precipi,precipm, condition, fog, rain, snow, hail, thunder, tornado))
	    except Exception as e:
		print "Problem inserting data into Weather Obs Table, probably a duplicate,skipping %s" % e
		#lgr.warning("Problem inserting data %s into Weather Obs Table %s, maybe a duplicate? Skipping. %s" % (rec,table,e))

	f.close()
	#need to not hit the interface that often
	time.sleep(6) # max of 10 calls per minute
	d += delta_inc
	print d
	count=count+1;
	print "No of days completed: ", count
    else:
	count = 0
	#time.pause(86400)  # this line was to wait after there had been 500 hits in one day.
c.commit()
c.close()

dirpath = os.path.dirname(__file__)
temp = os.path.split(dirpath)[0]+r"\sqlserver\update_nulls_obv_history.sql"
sqlscript = temp.replace("\\","/")
cursor2 = connection.cursor()

for line in open(sqlscript,'r'):
    cursor2.execute(line)

cursor2.commit()
cursor2.close()

print 'All done'

