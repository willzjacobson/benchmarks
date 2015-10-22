"""
This module reads the WX obs data from weatherunderground
"""

__version__ = '$Id'
__author__ = 'aboulanger@ccls.columbia.edu'

_module = 'wxobs'

import sys
import urllib2
import json
import datetime
import time
import odbc
from common_rudin import log_from_config, setup # common_fedex is giving errors
import optparse
import cfgparse

# see http://www.wunderground.com/weather/api/d/docs

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

mod_optgroup.add_option("--delta", type="int",
      help="how many days to truncate before adding WX data to the DB")
mod_cfggroup.add_option('delta', keys=_module)

mod_optgroup.add_option("--start", 
      help="Date (YYYY-MM-DD) to start populating the weather history. If the value is latest, will start from latest date in existing table")
mod_cfggroup.add_option('start', keys=_module)

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
delta_days = options.delta
start_date = options.start

lgr.info("Using these options %s %s %s %s %s %s %s %s %s %s" % (Driver,Server,Database,UID,PWD,table,api_key,location,delta_days,start_date))
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

db = odbc.odbc(CONNECTION_STRING)
c = db.cursor()

#f = urllib2.urlopen('http://api.wunderground.com/api/919d8958896c7e4e/hourly/q/NY/New_York.json')

#find out the last day in the database
#Will be using this for several offsets
#delta = datetime.timedelta(days=1)
delta = datetime.timedelta(days=delta_days)


today = datetime.datetime.today()
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
    #print 'last date in DB is %s' % row[0]
    lgr.info('last date in DB is %s' % row[0])
    last_day = row[0] - delta
    #last_day = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.0000000') - delta
    #start is one day before since we have 4 hrs of extra data (No longer)
    lgr.info('start date is %s' % last_day)
    cur_year = last_day.year
    cur_mo   = last_day.month
    cur_day  = last_day.day
    cur_date = datetime.datetime(cur_year,cur_mo,cur_day,0)
else:
    cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
       

#Use this to initialize the table
#cur_date = datetime.datetime(2012,03,30,0)

lgr.info( 'Deleting from %s' % (cur_date))
#DELETE FROM [dbo].[Weather_raw] WHERE date > '2012-08-15 04:00'
#delete any entries after our start date
query = "DELETE FROM [dbo].%s WHERE [date] >= ?" % (table)
try:
    c.execute (query, [cur_date])
except Exception as e:
    #print "Problem deleting data from Weather Obs Table %s" % e
    lgr.error("Attention: Problem deleting data from Weather Obs Table %s for date %s" % (table,cur_date))
    raise
    
url = 'http://api.wunderground.com/api/%s/history_%s/q/%s.json'
delta_inc = datetime.timedelta(days=1)
d = cur_date
while d <= today:
    url_date = d.strftime("%Y%m%d")
    lgr.info( 'Getting WX HX for %s' % url_date)
    url_res = url % (api_key, url_date, location)
    lgr.info( "Using this url: %s" % url_res)
    try:      
        f = urllib2.urlopen(url_res)
        json_string = f.read()
    except Exception as e:
        lgr.error("Attention: Error getting data for %s from Weather Underground API: Error %s, skipping day" % (url_date,e))
        continue
    try:
        parsed_json = json.loads(json_string)
        odata_list = parsed_json['history']['observations']
    except Exception as e:
        lgr.error("Attention: Error parsing jason data for %s from Weather Underground API: Error %s, skipping day" % (url_date,e))
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
            obs_temp        = odata['tempi']
            obs_dtemp       = odata['dewpti']
            iso_date    = '%s-%s-%s %s:%s:00' % (obs_year, obs_month, obs_day, obs_hour, obs_min)
            iso_utcdate = '%s-%s-%s %s:%s:00' % (obs_utcyear, obs_utcmonth, obs_utcday, obs_utchour, obs_utcmin)
            rec = "%s (%s) : %s %s" % (iso_date, iso_utcdate, obs_temp, obs_dtemp)
        except Exception as e:
            lgr.warning("Problem parsing obs record %s skipping. Error is %s" % (odata,e))
            continue
        query = "INSERT INTO [dbo].%s([Date],[UTC_Date],[Temp],[Dewp]) VALUES (?,?,?,?)" % (table)
        try: 
            c.execute(query, (iso_date, iso_utcdate, obs_temp, obs_dtemp))
        except Exception as e:
            #print "Problem inserting data into Weather Obs Table, probably a duplicate,skipping %s" % e
            lgr.warning("Problem inserting data %s into Weather Obs Table %s, maybe a duplicate? Skipping. %s" % (rec,table,e))
        print rec
    f.close()
    #need to not hit the interface that often
    time.sleep(10)
    d += delta_inc
        
c.close()
#print 'All done'
lgr.info("All done")
