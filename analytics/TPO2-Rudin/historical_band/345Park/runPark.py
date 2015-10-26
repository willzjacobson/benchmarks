import sys
import os
import datetime
import pyodbc
import optparse
import cfgparse
import traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spaceTemperature_trajectory.spaceTempTrajectory as spaceTempTrajectory
import data_tools.parkParameters as parkParameters
from common_rudin.common import log_from_config, setup, setup_cparser
from data_tools.configParser import paramConfigParser
import historical_band.historical_band as hb


__version__ = '$Id'
__author__ = 'vb2317@columbia.edu'
_module = 'historical_band'


def main(argv):
    #str_argv = "python C:\Rudin\historical_band\345Park\runPark C:\Rudin\data_tools\config_master.json 345_Park"
    if argv is None:
        argv = ' '.split(str_argv)
    if argv is None:
        argv = sys.argv
    argv = ["python", "C:\Rudin\historical_band\345Park\runPark.py", "C:\Rudin\data_tools\config.ini" ,"345_Park"]
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
    weatherDB = parser.weatherDB()
    weatherConnString='DRIVER={SQL SERVER};'+'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(server,weatherDB,uid,pwd)
    weatherConn=pyodbc.connect(weatherConnString) 
    weatherCursor=weatherConn.cursor()
    # parameters for commit
    tableName = parser.outputSpaceTempTrajectoryTable()
    paramObj = parkParameters.initializeParametersPark(configFile, configKey)
    now = datetime.datetime.now()
    gridSearchFlag = False
    performGridSearch = False
    Run_DateTime = now
    input_day = 2013106
    hb_obj = hb.HistBand(cursor,paramObj,weatherCursor,lgr)
    similar_weather_dates = hb_obj.get_similar_weather_dates(input_day)
    df_band = hb_obj.df[similar_weather_dates]
    upper_band = df_band.max(axis=1)
    lower_band = df_band.min(axis=1)
    hb_obj.write_band_to_db(hb_obj.df[input_day],upper_band,lower_band)
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.plot(hb_obj.df[input_day].index,hb_obj.df[input_day])
    #ax.plot(hb_obj.df[input_day].index,upper_band)
    #ax.plot(hb_obj.df[input_day].index,lower_band)
    #ax.set_xlabel("Steam (Mlb/hr)")
    #ax.grid(True,which='both')
    #plt.show()


if __name__ == '__main__':
    main(sys.argv)

