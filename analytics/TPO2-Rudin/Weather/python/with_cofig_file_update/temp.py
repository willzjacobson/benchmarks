'''
stub to read information from ini file.
'''

__version__ = '$Id'
__author__ = 'aboulanger@ccls.columbia.edu'

_module = 'wxobs'

import sys
import urllib2
import json
import datetime
import time
#import odbc
#from common_rudin import log_from_config, setup # common_fedex is giving errors
from common import setup, log_from_config
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
print CONNECTION_STRING
print table 
print api_key
print location