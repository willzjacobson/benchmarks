import data_tools.dataCollectors as dataCollectors
import data_tools.parkParameters as parkParameters
import data_tools.lexParameters as lexParameters
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
_module = 'occupancy_rampdown_bl'

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

    parser = paramConfigParser(configFile, configKey)
    server =parser.server()
    db =parser.database()
    uid = parser.uid()
    pwd = parser.pwd()
    connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
    conn=pyodbc.connect(connString) 
    cursor=conn.cursor()
    paramObj = None
    outputTable = None
    print "config key is " + str(configKey) +"\n\n\n"
    if configKey == '345_Park':
        paramObj = parkParameters.initializeParametersPark(configFile, configKey)
        outputTable = '345---------BusinessLogicOccupancyRampdown'
    elif configKey == '560_Lex':
        paramObj = lexParameters.initializeParametersLex(configFile, configKey)
        outputTable = '560---------BusinessLogicOccupancyRampdown'
    
    now = datetime.datetime.now() + datetime.timedelta(-17)
    if now.weekday() == 5 or now.weekday() == 6:
        print "weekend run, no occupancy based rampdown rec"
        print "exiting..."
        return

    OccupancyDataCollector = dataCollectors.dataCollectorOccupancyPredictions(conn, cursor, paramObj.occupancyParams.tableName, 3, datetime.datetime.combine(now.date(), datetime.time(23,59,59)), includeWeekends=True)
    OccupancyDataCollector.getData()

    relevantRampdownHours = (datetime.time(13,0,0), datetime.time(21,0,0))
    relevantOccupancyData = []
    if now.date() not in OccupancyDataCollector.rawDataKeyDay:
        print "today's occupancy data not recovered..."
        print "exiting..."
        return
    else:
        for ts, val in OccupancyDataCollector.rawDataKeyDay[now.date()]:
            if ts.time() > relevantRampdownHours[0] and ts.time() < relevantRampdownHours[1]:
                relevantOccupancyData.append((ts,val))

    # Occupancy data for day has been collected.  Business logic follows

    '''
    attempt 1: predict rampdown if negative gradient from 1-2 pm
    else: predict rampdown if 2 negative gradients from 2- end

    '''

    
    
    prevVal = None
    grad = None
    rdRec = None
    negGradCtr = None
    rules = [(datetime.time(14,0,0), 1), (datetime.time(16,0,0),2), (datetime.time(21,0,0),3)]
    for ts, val in relevantOccupancyData:
        if prevVal == None:
            prevVal = val
            continue
        else:
            grad = val-prevVal
            print "ts, grad is: " + str(ts) + ", "+ str(grad) +"..."

        #engage rules
        for blts, ctrVal in rules:
            if ts.time() < blts:
                if grad < 0:
                    if negGradCtr == None:
                        negGradCtr = 1
                    else:
                        negGradCtr += 1

                else:
                    negGradCtr =  None

                if negGradCtr >= ctrVal:
                    rdRec = ts
        if rdRec != None:
            break
    if rdRec == None:
        rdRec= datetime.time(21,0,0)
        rdRec = datetime.datetime.combine(datetime.datetime.now().date(), rdRec)
    

    print "rampdown rec: " + str(rdRec)

    try:
        commitPrediction(cursor, conn, datetime.datetime.now(), rdRec, outputTable)
    except:
        print "commit failed"


def commitPrediction(cursor, conn, runDateTime, predictionDateTime, tableName):
    query = "insert into " + tableName + "(Run_DateTime, Prediction_DateTime) values ('"
    query += runDatetime.strftime("%Y-%m-%d %H:%M") + "', '" + str(predictionDateTime) +"' )"
    try:
        cursor.execute(query)
        conn.commit()
    except:
        print "final commit failed... exiting"
        return
    print "rampdown time committed."
            


if __name__ == '__main__':
    main(sys.argv)
