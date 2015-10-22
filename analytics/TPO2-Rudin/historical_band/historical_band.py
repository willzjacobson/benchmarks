import numpy as np
import pandas as pd
import datetime as dt
from scipy.interpolate import interp1d
from trajectory_predictor.trajectoryPredictor import trajectoryPredictorBase
from data_tools.dataCollectors import *

class HistBand():
    def __init__(self, cursor, paramObj, weatherCursor,lgr):
        self.weekday_name = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
        self.cursor = cursor
        self.weatherCursor = weatherCursor
        self.paramObj = paramObj
        self.read_steam_db()
        self.read_weather_db()
        self.gen_dfs()
        self.lgr = lgr
        
    def read_steam_db(self):
        # read data from database
        query = 'SELECT TIMESTAMP,VALUE FROM {0} ORDER BY TIMESTAMP ASC'.format(self.paramObj.steamParams.tableName)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        rows = np.asarray(rows) 
        self.ts = pd.Series(rows[:,1],index=rows[:,0])
        return self.ts

    def read_weather_db(self):
        #read weather from database
        #TODO check weather columns names for temp and dewp
        #TODO CHECK between observed and forecaseted weather
        paramObj = self.paramObj
        weatherCursor = self.weatherCursor
        ts = self.ts
        date_fmt = '%Y-%m-%d %H:%M:%S'       
        query = 'SELECT Date, TempA, DewPointA FROM {0} ORDER BY Date ASC'.format(paramObj.weatherObsParams.tableName)
        weatherCursor.execute(query)
        rows = weatherCursor.fetchall()
        rows = np.asarray(rows)
        temps = np.asarray(map(float,rows[:,1]))
        dewps = np.asarray(map(float,rows[:,2]))
        # -8 to remove microseconds
        weather_dates = [np.datetime64(dt.datetime.strptime(item[:-8],date_fmt),'m') for item in rows[:,0]]
        weather_dates = np.asarray(weather_dates)
        #weathers = np.column_stack((weather_dates,temps,dewps))
        #npw = np.asarray(weathers)
        weather_dates = weather_dates[(temps>-1000)&(dewps>-1000)]
        temps2 = temps[(temps>-1000)&(dewps>-1000)]
        dewps = dewps[(temps>-1000)&(dewps>-1000)]
        temps = temps2
        #extract datetime 
        load_dates = np.asarray(ts.index.values)
        load_dates = np.asarray([np.datetime64(item,'m') for item in load_dates])
        #extract datetime in float format
        x = [(item).astype(long) for item in weather_dates]
        x_new = [(item).astype(long) for item in load_dates]
        if max(x)<max(x_new):
            npxn = np.asarray(x_new)
            #TODO change load_dates in the original method to least count as minute
            load_dates = load_dates[npxn<=max(x)]
            load_values = ts.values[npxn<=max(x)]
            self.ts = pd.Series(load_values,index=load_dates)
            x_new = npxn[npxn<=max(x)].tolist()
        x = map(long,x)
        x_new = map(long,x_new)
        f_temp = interp1d(x,temps)
        f_dewp = interp1d(x,dewps)
        temps = f_temp(x_new)
        dewps = f_dewp(x_new)
        self.wts = pd.Series(temps,index=load_dates)
        return self.wts

    def gen_dfs(self):
        ts = self.ts
        wts = self.wts
        hr = pd.Series(ts.index.map(lambda x: x.hour+(float(x.minute - (x.minute%15))/60)),index=ts.index)
        dod = pd.Series(ts.index.map(lambda x: int('%d%03d'%(x.year,x.dayofyear))),index=ts.
    index)
        df = pd.concat([ts,dod,hr],axis=1)
        df.columns=['ts','dod','hr']
        df = df.drop_duplicates(cols=['hr','dod'],take_last=True)
        df = df.pivot(columns='dod',index='hr',values='ts')
        print 'wts: %d dod: %d hr %d ts: %d'%(len(wts),len(dod),len(hr),len(ts))
        wdf = pd.concat([wts,dod,hr],axis=1)
        wdf.columns = ['wts','dod','hr']
        wdf = wdf.drop_duplicates(cols=['hr','dod'],take_last=True)
        wdf = wdf.pivot(columns='dod',index='hr',values='wts')
        self.df = df
        self.wdf = wdf
        return df,wdf

    def get_similar_weather_dates(self,input_day,start=-0.1,end=24.1,num=20):
        '''
        For the given input day, find the most similar weather days
        using L-1 distance
        input_day format: yyyydoy
        '''
        self.input_day = input_day
        #inputts = mydf[2013010]
        mywdf = self.wdf
        wdf = {}
        for x in mywdf.columns:
            if(dt.datetime.strptime(str(int(x)),'%Y%j').weekday() <= 4):
                wdf[x] = mywdf[x]
        mywdf = pd.DataFrame(wdf)
        mywdf = mywdf[(mywdf.index>=start) & (mywdf.index<=end)]
        inputts = mywdf[input_day]
        diffdf = mywdf.apply(lambda x:abs(x-inputts),axis=0).sum()
        diffdf.sort()
        dates = diffdf[:num].index
        #print dates
        days = [dt.datetime.strptime(str(int(item)),'%Y%j') for item in dates]
        #print days
        #mydf[dates].plot()
        weekdays = [self.weekday_name[item.weekday()] for item in days ]
        return dates

    def write_band_to_db(self,load,upper,lower):
        input_day = self.input_day
        cursor = self.cursor
        band_table = '345_Park_historical_band'
        dates= pd.date_range(dt.datetime.strptime(str(input_day),'%Y%j'),freq='15Min',periods=96)
        for i,item in enumerate(load):
            query = "INSERT INTO [{0}] VALUES('{1}',{2},{3},{4})".format(band_table,dates[i],load[i],upper[i],lower[i])
            #query = ' SELECT * FROM [{0}] WHERE 1=2'.format(band_table)
            print query
            cursor.execute(query)
        cursor.commit()
        cursor.close()
        self.lgr.info('Data succussfully inserted')
