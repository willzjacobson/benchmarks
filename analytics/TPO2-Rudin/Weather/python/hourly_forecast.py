__author__ = 'vanamali'

'''
This module reads the WX forecast data from weatherunderground
'''

_module = 'Forecast_NY_KNYC'

import os
import sys
import urllib2
import json
from datetime import datetime, timedelta
import time
import pyodbc
from pytz import timezone
import pytz
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
      help="db driver name, ")
mod_cfggroup.add_option('driver', keys=_module)

mod_optgroup.add_option("--server", 
      help="db server name, ")
mod_cfggroup.add_option('server', keys=_module)

mod_optgroup.add_option("--database", 
      help="db database name, ")
mod_cfggroup.add_option('database', keys=_module)

mod_optgroup.add_option("--UID", 
      help="db user name, ")
mod_cfggroup.add_option('UID', keys=_module)

mod_optgroup.add_option("--PWD", 
      help="db user password, ")
mod_cfggroup.add_option('PWD', keys=_module)

mod_optgroup.add_option("--table", 
      help="db table name, ")
mod_cfggroup.add_option('table', keys=_module)

mod_optgroup.add_option("--api_key", 
      help="API key, get one from http://api.wunderground.com/api")
mod_cfggroup.add_option('api_key', keys=_module)

mod_optgroup.add_option("--location", 
      help="location use  NY/New_York or KNYC for Central Park, KLGA is LaGuardia, pws:KNYBROOK40 is a Williamsburg, for example, personal station ")
mod_cfggroup.add_option('location', keys=_module)

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

eastern = timezone('US/Eastern')
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
utc = pytz.utc
today = eastern.localize(datetime.today())
today_utc = today.astimezone(utc)


CONNECTION_STRING ="""
Driver=%s;
Server=%s;
Database=%s;
UID=%s;
PWD=%s;
Trusted_Connection=No;
""" % (Driver, Server, Database, UID, PWD)

# pyodbc
connection = pyodbc.connect(CONNECTION_STRING)
c = connection.cursor()

'''
#test connection
print CONNECTION_STRING
query ="select COUNT(*) from Hourly_Forecast"
c.execute(query)
for row in c.fetchall():
	print row[0]
'''

url = 'http://api.wunderground.com/api/%s/hourly/q/%s.json' % (api_key, location)
#lgr.info('Using this url: %s' % url)
print 'Using this url: %s' % url
#lgr.info('Getting WX Forecast for %s' % today)
print 'Getting WX Forecast for %s' % today
try:
    f = urllib2.urlopen(url)
    json_string = f.read()
except Exception as e:
        #lgr.error("Error getting forecast for %s from Weather Underground API %s: Error %s, quitting" % (today,url,e))
        print "Error getting forecast for %s from Weather Underground API %s: Error %s, quitting" % (today,url,e)
        #f.close()
        c.close()
        raise
try:
    parsed_json = json.loads(json_string)
    fdata_list = parsed_json['hourly_forecast']
except Exception as e:
        #lgr.error("Error parsing jason forecast for %s from Weather Underground API: Error %s, quitting" % (today,e))
        print "Error parsing jason forecast for %s from Weather Underground API: Error %s, quitting" % (today,e)
        f.close()
        c.close()
        raise
#print fdata_list

for fdata in fdata_list:
    try:
        forecast_min    =   fdata['FCTTIME']['min']
        forecast_hour   =   fdata['FCTTIME']['hour_padded']
        forecast_day    =   fdata['FCTTIME']['mday_padded']
        forecast_month  =   fdata['FCTTIME']['mon_padded']
        forecast_year   =   fdata['FCTTIME']['year']

        fctempm  =   fdata['temp']['metric']
        fctempi  =   fdata['temp']['english']

        fcdewm    =   fdata['dewpoint']['metric']
        fcdewi    =   fdata['dewpoint']['english']

        fccond   =   fdata['condition']
        fcsky    =   fdata['sky']

        fcwspdm   =   fdata['wspd']['metric']
        fcwspdi   =   fdata['wspd']['english']

        fcwdir   =   fdata['wdir']['degrees']
        fcwx     =   fdata['wx']
        fcuvi    =   fdata['uvi']
        fchum    =   fdata ['humidity']

        fcwchillm =   fdata['windchill']['metric']
        fcwchilli =   fdata['windchill']['english']

        fchindexm =   fdata['heatindex']['metric']
        fchindexi =   fdata['heatindex']['english']

        fcfeelsm  =   fdata ['feelslike']['metric']
        fcfeelsi  =   fdata ['feelslike']['english']

        fcqpfm    =   fdata['qpf']['metric']
        fcqpfi    =   fdata['qpf']['english']

        fcsnowm  =   fdata['snow']['metric']
        fcsnowi   =   fdata['snow']['english']
        
        fcpop    =   fdata['pop']

        fcmslpm   =   fdata['mslp']['metric']
        fcmslpi   =   fdata['mslp']['english']

	#start at 4AM UTC
	iso_date = '%s-%s-%s %s:%s' % (forecast_year, forecast_month, forecast_day, forecast_hour, forecast_min)
	iso_date = eastern.localize(datetime.strptime(iso_date, '%Y-%m-%d %H:%M'))
	iso_utcdate = iso_date.astimezone(utc)
	rec = "%s (%s) %s (%s)" % (today, today_utc, iso_date, iso_utcdate)
    except Exception as e:
        #lgr.warning("Problem parsing forecast record %s skipping. Error is %s" % (fdata,e))
        print "Problem parsing forecast record %s skipping. Error is %s" % (fdata,e)
        continue
    print 
    query = "INSERT INTO [dbo].%s([Fcst_date],[Fcst_UTC_Date],[Date],[UTC_Date],[TempA],[TempM],[DewA],[DewM],[Condition],[Sky],[WSpeedA],[WSpeedM],[WDir],[WX],[UVI],[Humidity],[WindChillA],[WindChillM],[HeatIndexA],[HeatIndexM],[FeelsLikeA],[FeelsLikeM],[QPFA],[QPFM],[SnowA],[SnowM],[POP],[MSLPA],[MSLPM]) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % table
    try:
        print 'inserting record'
        c.execute (query, (today, today_utc, iso_date,iso_utcdate, fctempi,fctempm, fcdewi,fcdewm, fccond, fcsky, fcwspdi,fcwspdm, fcwdir, fcwx, fcuvi, fchum, fcwchilli, fcwchillm, fchindexi,fchindexm, fcfeelsi,fcfeelsm, fcqpfi,fcqpfm, fcsnowi,fcsnowm, fcpop, fcmslpi,fcmslpm))
    except Exception as e:
        #lgr.warning("Problem inserting data %s into Weather Forecast Table %s. Skipping %s" % (table,rec,e))
        print "Problem inserting data %s into Weather Forecast Table %s. Skipping %s" % (table,rec,e)

f.close()
c.commit()
c.close()


dirpath = os.path.dirname(__file__)
temp = os.path.split(dirpath)[0]+r"\sqlserver\update_nulls_hourly_update.sql"
sqlscript = temp.replace("\\","/")
cursor2 = connection.cursor()

for line in open(sqlscript,'r'):
    cursor2.execute(line)

cursor2.commit()
cursor2.close()

print 'All done'
#lgr.info('All done')
