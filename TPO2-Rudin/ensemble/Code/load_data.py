__version__='$Id'
__author__= 'Vaibhav Bhandari <vb2317@columbia.edu>'
_module='load_data'

import pyodbc
import optparse
import cfgparse
import datetime as dt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from abc import ABCMeta,abstractmethod

import data_module as bh
import load_data as ld
import spaceTemperature_trajectory.spaceTempTrajectory as spaceTempTrajectory
import data_tools.parkParameters as parkParameters
from common_rudin.common import log_from_config, setup, setup_cparser
from data_tools.configParser import paramConfigParser
import historical_band.historical_band as hb

class DataReader(object):
    '''
    This is an abstract class
    This class should be inherited to create any data readers

    Arguments
    ---------
    None
    
    Methods
    -------
    instantiate : returns a concrete instance of subclass after reading the config file

    Examples
    --------
    '''
    __metaclass__=ABCMeta

    def __init__(self):
        pass

    @classmethod
    def instantiate(cls,argv=None,**keywords):
        '''
        This is a classmethod
        It returns an instance of subclass of DataReader
        This method reads the config file
        '''
        #TODO change argv hardcoding
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
        run_ts = dt.datetime.now()
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
        #dr_obj = ld.DataReaderDbSteam(cursor,paramObj,lgr)
        #dr_obj = ld.DataReaderCsvSteam(logger=lgr)
        #steam_obj =bh.Steam(read_from_db=True,data_reader_obj=dr_obj)
        #print steam_obj.df
        #dr_obj = ld.DataReaderDbWeather(weatherCursor,paramObj,lgr)
        #dr_obj = ld.DataReaderCsvWeather(logger=lgr)
        #weather_obj = bh.Weather(data_reader_obj=dr_obj)
        #print weather_obj.df
        if 'filename' in keywords:
            filename=keywords['filename']
        else:
            filename=None
        if 'date_fmt' in keywords:
            date_fmt = keywords['date_fmt']
        else:
            date_fmt=None
        return cls(cursor=cursor,weatherCursor=weatherCursor,paramObj=paramObj,logger=lgr,filename=filename,date_fmt=date_fmt)

    def __init__(self,**keywords):
        self.cursor=keywords['cursor']
        self.weatherCursor=keywords['weatherCursor']
        self.paramObj=keywords['paramObj']
        self.logger=keywords['logger']
        self.filename=keywords['filename']
        self.date_fmt=keywords['date_fmt']

    @abstractmethod
    def read_data(self):
        '''
        This method should be implemented by every subclass that is not abstrct
        '''
        pass


class DataReaderDb(DataReader):
    '''
    This is a generic concrete class for a Database reader

    Arguments
    ---------
    cursor: cursor to the database 
    paramObj: from config file
    logger: logger object

    Methods
    ----------
    read_data: reads data from db

    Examples
    --------

    '''
    def __init__(self,**keywords):
        super(DataReaderDb,self).__init__(**keywords)
        self.logger.info('%s: DB Reader initializing'%_module)

    def read_data(self,query=''):
        '''
        This method implements a generic reader from Database
        '''
        if len(query)==0:
            raise ValueError('%s: Invalid SELECT query'%(_module)) 
        self.query=query
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        rows = np.asarray(rows) 
        self.rows = rows

class DataReaderDbSteam(DataReaderDb):
    '''
    This is a concrete class for Steam Database reader

    Arguments
    ---------
    cursor      : cursor to the database 
    paramObj    : from config file
    logger      : logger object

    Method
    ----------
    read_data   : reads Steam data from db

    Examples
    --------

    '''
    def __init__(self,**keywords):
        super(DataReaderDbSteam,self).__init__(**keywords)

    def read_data(self):
        '''
        Reads data from Steam database
        '''
        query = 'SELECT TIMESTAMP,VALUE FROM {0} ORDER BY TIMESTAMP ASC'.format(self.paramObj.steamParams.tableName)
        self.query=query
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        rows = np.asarray(rows) 
        self.rows = rows[:,0:2].tolist()

class DataReaderDbWeather(DataReaderDb):
    '''
    This is a concrete class for Weather Database reader

    Arguments
    ---------
    cursor      : cursor for weather database
    paramObj    : from config file
    logger         : logger object

    Method
    ----------
    read_data: reads data from db

    Examples
    --------

    '''
    def __init__(self,**keywords):
        super(DataReaderDbWeather,self).__init__(**keywords)

    def read_data(self):
        #read weather from database
        #TODO check weather columns names for temp and dewp
        #TODO CHECK between observed and forecaseted weather
        paramObj = self.paramObj
        cursor = self.weatherCursor
        query = 'SELECT Date, TempA, DewPointA FROM {0} ORDER BY Date ASC'.format(paramObj.weatherObsParams.tableName)
        cursor.execute(query)
        rows = np.asarray(cursor.fetchall())
        self.rows = rows[:,0:3].tolist()
        
        
class DataReaderCsv(DataReader):
    '''
    This is a generic concrete class for CSV reader

    Arguments
    ---------
    filename    : filename for the csv
    date_fmt    : date format of dates inside csv
    logger         : logger

    Method
    ----------
    read_data: reads Steam data from csv

    Examples
    --------
    '''
    def __init__(self,**keywords):
        super(DataReaderCsv,self).__init__(**keywords)
    
    def read_data(self):
        pass

class DataReaderCsvSteam(DataReaderCsv):
    '''
    This is concrete class for CSV reader for Steam Data

    Arguments
    ---------
    filename    : csv filename for Steam data 
    date_fmt    : date format of dates inside steam csv
    logger      : logger

    Method
    ----------
    read_data: reads Steam data from csv

    Examples
    --------
    '''
    def __init__(self,**keywords):
        super(DataReaderCsvSteam,self).__init__(**keywords)
        date_fmt = self.date_fmt
        filename = self.filename
        if date_fmt is None:
            date_fmt="%Y-%m-%d %H:%M:%S.%f"
        if filename is None:
            filename="../Data/RUDINSERVER_CURRENT_STEAM_DEMAND_FX70_AUG.csv"
        self.filename=filename
        self.date_fmt = date_fmt

    def read_data(self):
        '''
        Arguments
        ---------
        date_fmt: Date format
        filename: dir path + filename of input file
        '''
        filename=self.filename
        date_fmt=self.date_fmt
        f = open(filename,'rU')
        steam_data = []
        cnt = 0
        for line in f:
            vals = line.rstrip().split(',')
            try:
                vals[1] = vals[1][:23] #trim microseconds to 3 digits
                steam_date = dt.datetime.strptime(vals[1],date_fmt) 
                steam_data.append((steam_date,float(vals[2])))
            except:
                print vals[1],'val: ',vals[2]
                print "INCORRECT DATETIME FORMAT"
                cnt += 1
        f.close()
        print 'Count: %d'%(cnt)
        self.rows = steam_data

class DataReaderCsvWeather(DataReaderCsv):
    '''
    This is concrete class for CSV reader for Weather Data

    Arguments
    ---------
    filename    : csv filename for Weather data 
    date_fmt    : date format of dates inside Weather csv
    logger      : logger

    Method
    ----------
    read_data: reads Weather data from csv

    Examples
    --------
    '''
    def __init__(self,**keywords):
        super(DataReaderCsvWeather,self).__init__(**keywords)
        filename=self.filename
        date_fmt=self.date_fmt
        if date_fmt is None:
            date_fmt="%Y-%m-%d %H:%M:%S.%f"
        if filename is None:
            filename="../Data/OBSERVED_WEATHER_AUG.csv"
        self.filename=filename
        self.date_fmt = date_fmt

    def read_data(self):
        '''
        args:
        date_fmt = date format
        filename = csv filename for weather data
        '''
        filename = self.filename
        date_fmt = self.date_fmt
        f = open(filename,'rU')
        weather_data = []
        for line in f:
            vals = line.rstrip().split(',')
            try:
                vals[1] = vals[1][:23] #trim microseconds to 3 digits
                weather_date = dt.datetime.strptime(vals[1],date_fmt) 
                weather_data.append((weather_date,vals[2],vals[4]))
            except:
                print "INCORRECT DATETIME FORMAT"
        f.close()
        weather_data.reverse() #change the sorted order to asc
        self.rows = weather_data

def main():
    pass

if __name__=='__main__':
    main()
