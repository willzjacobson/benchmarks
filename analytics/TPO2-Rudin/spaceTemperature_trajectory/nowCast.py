import spaceTemperature_trajectory.spaceTempTrajectory as spaceTempTrajectory
import data_tools.dataCollectors as dataCollectors
import data_tools.configObject as configObject
import sys
import os
import datetime
import pyodbc
import optparse
import cfgparse
import traceback
import forecast


from common_rudin.common import log_from_config, setup, setup_cparser
from data_tools.configParser import paramConfigParser


__version__ = '$Id'
__author__ = 'anr2121@columbia.edu'
_module = 'nowCast'


def main(argv):
    if argv is None:
        argv = sys.argv

    if len(argv) < 3 or len(argv) > 4:
        print "usage: python nowCast.py building configFileLoc [gridSearch]"
        print "current building options: 345_Park, 560_Lex, 40E52, 1BP"
        print "grid Search is an optional parameter"
        return


    configFile = argv[2]
    configKey = argv[1]


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


    # parameters for commit
    tableName = configObj.sptTrajectoryParams.outputSptTrajectory


    paramObj = configObj

    ###
    # get nowCast Params
    ###
    
    now = datetime.datetime.now() #+ datetime.timedelta(0,-120)
    gridSearchFlag = False
    if len(argv) > 3:
        if argv[3] == "gridSearch":
            gridSearchFlag = True
            performGridSearch = True
            lgr.info('running grid search, no data will be committed')
        else:
            print "third input argument detected, but not understood.  Continuing without performing grid search"
            performGridSearch = False
    else:
        performGridSearch = False
    Run_DateTime = now

    relevantHours = (datetime.time(0, 00), datetime.time(23,59)) # we want 24/7 predictions

    ###
    # run nowCast
    ###

    try:
        trajectoryPredictor = spaceTempTrajectory.universalTrajectoryPredictor(conn, cursor, paramObj, 14, now, 1, performGridSearch,
                                                 [8, 4, 2, 1],  relevantHours)
        trajectoryPredictor.readFromDB()
        trajectoryPredictor.autorun()
        lgr.info('timestep 1 calculated')
    except:
        lgr.critical('An error occurred in timestep 1: %s' % traceback.format_exc())

    now = trajectoryPredictor.maxTS
    predictionTimeBase = now
    now = now + datetime.timedelta(0, 120)

    trajectoryPredictorKeyTimestep = {}
    trajectoryPredictorKeyTimestep[1] = trajectoryPredictor
    for timestep in range(2,9):
        try:
            trajectoryPredictorKeyTimestep[timestep] = spaceTempTrajectory.universalTrajectoryPredictor(conn, cursor, paramObj,
                                                                        14, now, timestep, performGridSearch,
                                                                        [8, 4, 2, 1], relevantHours)
            trajectoryPredictorKeyTimestep[timestep].borrowData(trajectoryPredictor)
            trajectoryPredictorKeyTimestep[timestep].autorun()
            lgr.info('timestep %s calculated' % str(timestep))
        except:
            lgr.critical('An error occurred in timestep %s: %s' % (str(timestep), traceback.format_exc()))
    if gridSearchFlag == False:
        for timestep in trajectoryPredictorKeyTimestep:
            trajectoryPredictorKeyTimestep[timestep].commitPredictionsSQL(tableName, predictionTimeBase, Run_DateTime)
        lgr.info('predictions committed')
    else:
        lgr.info('grid search complete')

if __name__ == '__main__':
	building = sys.argv[1]
	try:
		main(sys.argv)
	except:
		print "Secondary System is being invoked."
		if building == '345_Park':
			config_key = 'Rudin_345Park'
		if building == '560_Lex':
			config_key = 'Rudin_560Lexington'
		if building == '40E52':
			config_key = 'Rudin_40E52'
		if building == '1BP':
			config_key = 'Rudin_1BP'
		if building == 'Rudin_WHI':
			config_key = 'Rudin_WHI'
		if building == 'Rudin_641':
			config_key = 'Rudin_641LE'
		
		forecast.forecast("C:\\Rudin\\config_master.json", config_key)

    
