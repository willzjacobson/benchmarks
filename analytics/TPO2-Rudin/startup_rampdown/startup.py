from startup_rampdown.startupPredictor import universalStartupPredictor
import data_tools.dataCollectors as dataCollectors
import data_tools.configObject as configObject
import sys
import os
import datetime
import pyodbc
import optparse
import cfgparse
import traceback

from common_rudin.common import log_from_config, setup, setup_cparser
from data_tools.configParser import paramConfigParser

import fallback_logic.tfailover as failover

__version__ = '$Id'
__author__ = 'anr2121@columbia.edu'
_module = 'startup'



def main(argv):
    if argv is None:
        argv = sys.argv

    if len(argv) != 3:
        print "usage: python startup.py building configFileLoc"
        print "current building options: 345_Park, 560_Lex, 40E52, 1BP" 
        return

    

    configFile = argv.pop()
    configKey = argv.pop()

    ###
    # Boilerplate to set up cParser
    ###
    version = "%prog 0.1"
    usage = "usage: %prog [options]"

    oparser = optparse.OptionParser(usage=usage, version=version,
	    description=__doc__)
    cparser = cfgparse.ConfigParser()


    setup(oparser, cparser, _module)

    options, args = cparser.parse(oparser, argv)


    lgr = log_from_config(options, _module)
    lgr.info('*** %s starting up' % _module)
	
    arg_count = len(args)

    run_ts = datetime.datetime.now()
    lgr.info('run time: %s' % run_ts)


    ###
    # Set up Config Options
    ###
    
    configObj = configObject.configObject(configFile, configKey)
    configObj.getObject()
    server = configObj.server
    db = configObj.db
    uid = configObj.uid
    pwd = configObj.pwd
    connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
    conn=pyodbc.connect(connString) 
    cursor=conn.cursor()


    paramObj = configObj
    now = datetime.datetime.now()# + datetime.timedelta(-1)
    performGridSearch = True


    ###
    # today/next day selection
    ###
    if now.time() > datetime.time(8,00):
        now = now+datetime.timedelta(1)
    if now.weekday() == 5 or now.weekday()==6:
        lgr.info("weekend run, no startup time, canceling")
        print "weekend run, no startup time, cancelling"
        return 0

    relevantHours = (datetime.time(4, 00), datetime.time(8,00))


    ###
    # run startup
    ###

    print now
    try:
        startupPred = universalStartupPredictor(conn, cursor, paramObj, 21, now,
                                                                      1, performGridSearch,
                                                                      [16, 8, 6, 4, 3, 2, 1],  relevantHours)
        startupPred.readFromDB()
        startupPred.autorun()
        final = startupPred.commitFinalPrediction()
        lgr.info("prediction recorded as: %s", str(final))

    except:
        lgr.critical('An error occurred while predicting startup: %s' % traceback.format_exc())

        #_configFile = 'C:\\Rudin\\fallback_logic\\config.ini'
        failover.fall_back(configFile, configKey, 'startup', lgr)

    
if __name__ == '__main__':
    main(sys.argv)


    





    
