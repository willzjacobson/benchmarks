from startup_rampdown.rampdownPredictor import rampdownPredictorPark
import data_tools.dataCollectors as dataCollectors
import data_tools.parkParameters as parkParameters
import data_tools.parameterObject as parameterObject
import sys
import os
import datetime
import pyodbc
import optparse
import cfgparse
import traceback

from common_rudin.common import log_from_config, setup, setup_cparser
from data_tools.configParser import paramConfigParser


__version__ = '$Id'
__author__ = 'anr2121@columbia.edu'
_module = 'park_rampdown'



def main(argv):
    if argv is None:
        argv = sys.argv

    configKey = argv.pop()
    configFile = argv.pop()

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

    #TODO: Read from config
    parser = paramConfigParser(configFile, configKey)
	
    server = parser.server()
    db = parser.database()
    uid = parser.uid()
    pwd = parser.pwd()
    connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
    conn=pyodbc.connect(connString) 
    cursor=conn.cursor()

    # parameters for commit
    outputTable = parser.outputRampDownTable()

    paramObj = parkParameters.initializeParametersPark(configFile, configKey)
    now = datetime.datetime.now()
    performGridSearch = True
    if now.time() > datetime.time(21,00):
        now = now+datetime.timedelta(1)
    else:
        now = datetime.datetime.combine(now.date(), datetime.time(23,59))
    if now.weekday() == 5 or now.weekday()==6:
        print "weekend run, no rampdown time, cancelling"
        lgr.info("weekend run, no rampdown time, canceling")
        return 0


    relevantHours = (datetime.time(13, 00), datetime.time(21,00))

    try:
    
        rampdownPred = rampdownPredictorPark(conn, cursor, paramObj, 14, now,
                                                                      1, performGridSearch,
                                                                      [8, 4, 2, 1],  relevantHours)
        rampdownPred.readFromDB()
        rampdownPred.autorun()
        rampdownPred.commitFinalPrediction(outputTable)
        lgr.info("prediction recorded as: %s", str(rampdownPred.finalPrediction))
    except:
        lgr.critical('An error occurred while predicting startup: %s' % traceback.format_exc())

    
if __name__ == '__main__':
	main(sys.argv)



    

