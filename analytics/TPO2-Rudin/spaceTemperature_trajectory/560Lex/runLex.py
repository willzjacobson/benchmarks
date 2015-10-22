import spaceTemperature_trajectory.spaceTempTrajectory as spaceTempTrajectory
import data_tools.dataCollectors as dataCollectors
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
_module = 'lex_spaceTemperature_trajectory'


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

    server = parser.server()
    db = parser.database()
    uid = parser.uid()
    pwd = parser.pwd()
    connString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,db,uid,pwd)
    conn=pyodbc.connect(connString) 
    cursor=conn.cursor()

    # parameters for commit
    tableName = parser.outputSpaceTempTrajectoryTable()


    paramObj = lexParameters.initializeParametersLex(configFile, configKey)
    now = datetime.datetime.now()
    gridSearchFlag = False
    if len(argv) > 1:
        if argv[1] == "gridSearch":
            gridSearchFlag = True
            performGridSearch = True
            lgr.info('running grid search, no data will be committed')
    else:
        performGridSearch = False
    Run_DateTime = now

    relevantHours = (datetime.time(0, 00), datetime.time(23,59)) # we want 24/7 predictions

    try:
        trajectoryPredictor = spaceTempTrajectory.trajectoryPredictorSptLex(conn, cursor, paramObj, 14, now, 1, performGridSearch,
                                                 [8, 4, 2, 1],  relevantHours, os.path.dirname(os.path.abspath(__file__))+'\\')
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
            trajectoryPredictorKeyTimestep[timestep] = spaceTempTrajectory.trajectoryPredictorSptLex(conn, cursor, paramObj,
                                                                        14, now, timestep, performGridSearch,
                                                                        [8, 4, 2, 1], relevantHours, os.path.dirname(os.path.abspath(__file__))+'\\')
            trajectoryPredictorKeyTimestep[timestep].borrowData(trajectoryPredictor.SptDataCollector,
                                                              trajectoryPredictor.SptPredictionsDataCollector,
                                                              trajectoryPredictor.RatDataCollector)
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
	main(sys.argv)



    
