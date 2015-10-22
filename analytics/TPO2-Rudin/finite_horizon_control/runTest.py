import spaceTempPark_state as spaceTempPark_state
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

from rpy2 import robjects


from common_rudin.common import log_from_config, setup, setup_cparser
from data_tools.configParser import paramConfigParser


__version__ = '$Id'
__author__ = 'anr2121@columbia.edu'
_module = 'park_finiteControlTest'


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

    paramObj = parkParameters.initializeParametersPark(configFile, configKey)
    
    now = datetime.datetime.now()

    mystate = spaceTempPark_state.spaceTempPark_state(conn,cursor, paramObj, 14, now)
    mystate.readFromDB()
    mystate.generateCovariates()
    mystate.matrixify()
    mystate.writeMatricesToFile()
    mystate.trainGP()

    #gpState_R = robjects.r("source('stateGP.R')")
    #agp = robjects.r("stateGP('C:/Rudin/finite_horizon_control/state/dataMatrices/XF02.csv', 'C:/Rudin/finite_horizon_control/state/dataMatrices/yF02.csv', 'F02')")

if __name__ == '__main__':
	main(sys.argv)
