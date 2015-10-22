"""
This module reads the WX forecast data from weatherunderground
"""

__version__ = '$Id'
__author__ = 'aboulanger@ccls.columbia.edu'

_module = 'wxfcst'

import sys
import urllib2
import json
from datetime import datetime, timedelta
import time
import odbc
from pytz import timezone
import pytz
from common.common import log_from_config, setup
import optparse
import cfgparse

#import dateutil
#import pytz

#
# see http://www.wunderground.com/weather/api/d/docs
#
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
      help="db driver name, use {SQL Native Client} for mssql")
mod_cfggroup.add_option('driver', keys=_module)

mod_optgroup.add_option("--server", 
      help="db server name, use joule.ldeo.columbia.edu at CCLS")
mod_cfggroup.add_option('server', keys=_module)

mod_optgroup.add_option("--database", 
      help="db database name, use GE for CCLS")
mod_cfggroup.add_option('database', keys=_module)

mod_optgroup.add_option("--UID", 
      help="db user name, use FedEx_db for CCLS")
mod_cfggroup.add_option('UID', keys=_module)

mod_optgroup.add_option("--PWD", 
      help="db user password, use fedex_trucks for CCLS")
mod_cfggroup.add_option('PWD', keys=_module)

mod_optgroup.add_option("--table", 
      help="db table name, use Weather_raw for CCLS")
mod_cfggroup.add_option('table', keys=_module)
 
mod_optgroup.add_option("--api_key", 
      help="API key, use 919d8958896c7e4e (AGB's key) or get one from http://api.wunderground.com/api")
mod_cfggroup.add_option('api_key', keys=_module)

mod_optgroup.add_option("--location", 
      help="location use  NY/New_York or KNYC for Central Park, KLGA is LaGuardia, pws:KNYBROOK40 is a Williamsburg, for example, personal station ")
mod_cfggroup.add_option('location', keys=_module)

(options, args) = cparser.parse(parser, argv)  
lgr = log_from_config(options, _module)        

lgr.info('*** %s starting up' % _module)
#lgr.debug('opening my_netrms with %s' % options.netrms_db)
#lgr.debug(par)

Driver = options.driver
Server = options.server
Database = options.database
UID = options.UID
PWD = options.PWD
table = options.table
#url = options.url
api_key = options.api_key
location = options.location

lgr.info("Using these options %s %s %s %s %s %s %s %s" % (Driver,Server,Database,UID,PWD,table,api_key,location))
#print (Driver,Server,Database,UID,PWD,delta_days)

#Driver = "{SQL Native Client}"
#Server = "joule.ldeo.columbia.edu"
#Database = "GE"
#UID = "FedEx_db"
#PWD = "fedex_trucks"

CONNECTION_STRING ="""
Driver=%s;
Server=%s;
Database=%s;
UID=%s;
PWD=%s;
Trusted_Connection=No;
""" % (Driver, Server, Database, UID, PWD) 

#if argv is None:
argv = sys.argv
      
eastern = timezone('US/Eastern')
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
utc = pytz.utc
today = eastern.localize(datetime.today())
today_utc = today.astimezone(utc)

db = odbc.odbc(CONNECTION_STRING)
c = db.cursor()


#api_key = '919d8958896c7e4e'
#location ='NY/New_York'
url = 'http://api.wunderground.com/api/%s/hourly/q/%s.json' % (api_key, location)
lgr.info('Using this url: %s' % url)
lgr.info('Getting WX Forecast for %s' % today)
#print 'Getting WX Forecast for %s' % today
try:
    f = urllib2.urlopen(url)
    json_string = f.read()
except Exception as e:
        lgr.error("Error getting forecast for %s from Weather Underground API %s: Error %s, quitting" % (today,url,e))
        f.close()
        c.close()
        raise
try:
    
    parsed_json = json.loads(json_string)
    fdata_list = parsed_json['hourly_forecast']
except Exception as e:
        lgr.error("Error parsing jason forecast for %s from Weather Underground API: Error %s, quitting" % (today,e))
        f.close()
        c.close()
        raise


for fdata in fdata_list:
    try:
        forecast_min    = fdata['FCTTIME']['min']
        forecast_hour   = fdata['FCTTIME']['hour_padded']
        forecast_day    = fdata['FCTTIME']['mday_padded']
        forecast_month  = fdata['FCTTIME']['mon_padded']
        forecast_year   = fdata['FCTTIME']['year']
        forecast_temp   = fdata['temp']['english']
        forecast_dtemp  = fdata['dewpoint']['english']
        #start at 4AM
        #date = datetime.datetime(forecast_year,forecast_month,forecast_day,forecast_hour,forecast_min)
        iso_date = '%s-%s-%s %s:%s:00' % (forecast_year, forecast_month, forecast_day, forecast_hour, forecast_min)
        iso_date = eastern.localize(datetime.strptime(iso_date, '%Y-%m-%d %H:%M:%S'))
        iso_utcdate = iso_date.astimezone(utc)
        rec = "%s (%s) %s (%s): %s %s" % (today, today_utc, iso_date, iso_utcdate, forecast_temp, forecast_dtemp)
    except Exception as e:
        lgr.warning("Problem parsing forecast record %s skipping. Error is %s" % (fdata,e))
        continue
    query = "INSERT INTO [dbo].%s([Fcst_date],[Fcst_UTC_Date],[Date],[UTC_Date],[Temp],[Dewp]) VALUES (?,?,?,?,?,?)" % table
    try:
        #print 'inserting record'
        c.execute (query, (today, today_utc, iso_date,iso_utcdate, forecast_temp, forecast_dtemp))
    except Exception as e:
        lgr.warning("Problem inserting data %s into Weather Fcst Table %s. Skipping %s" % (table,rec,e))
    print rec
    
f.close()
c.close()
#print 'All done'
lgr.info('All done')
