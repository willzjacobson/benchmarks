__author__= 'Vaibhav Bhandari vb2317@columbia.edu'
__module__= 'data_module'

from os import path
from abc import ABCMeta,abstractmethod
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import copy
from sklearn.hmm import GaussianHMM

DEBUG=False

class HMMCreator(object):
    '''
    Factory Class to create HMM objects
    
    Arguments
    ---------
    n_states            : number of states in the HMM model
    from_date           : start date for data
    to_date             : end date for data
    forecast_time_delta : no of days to be predicted
    hmm_obj             : hmm model object, if already present

    Parameters
    ----------
    from_date               : start date of training data
    to_date                 : end date of training data
    steam_obj               : object of Data class (subclass: Steam)
    weather_obj             : object of Data class (subclass: Weather)
    wobj_forecast           : object of Data class containing forecast data (subclass: Weather)
    sobj_forecast           : object of steam class containing forecast data (DEBUG mode only)
    hmm_obj                 : object of Data class (subclass: HMM)
    states_forecast         : list containing forecasted states
    states_forecast_steam   : list containing forecasted states (DEBUG mode only)

    Methods
    -------
    instantiate                 : class method that returns the object of this class 
    get_similar_states_dates    : returns dates (of days) that have similar states

    Examples
    --------
    '''
    @classmethod
    def instantiate(cls,n_states,from_date=dt.date(2012,2,1),to_date=dt.date(2013,7,9),forecast_time_delta=1,hmm_obj=None,steam_obj=None,weather_obj=None,wobj_forecast=None,sobj_forecast=None):
        return cls(n_states,from_date,to_date,forecast_time_delta,hmm_obj,steam_obj,weather_obj,wobj_forecast,sobj_forecast)

    def __init__(self,n_states,from_date,to_date,forecast_time_delta,hmm_obj,steam_obj,weather_obj,wobj_forecast,sobj_forecast):
        if hmm_obj==None:
            hmm_obj = HMM(steam_obj=steam_obj,weather_obj=weather_obj,n_states=n_states)
            hmm_obj.build_model()
            hmm_obj.build_forecast_model() 
        df_weather_forecast, X_weather_forecast= hmm_obj.gen_meta_data(weather_obj=wobj_forecast)
        if DEBUG:
            df_steam_forecast, X_steam_forecast= hmm_obj.gen_meta_data(steam_obj=sobj_forecast,weather_obj=wobj_forecast)
            states_forecast_steam = hmm_obj.model.predict(X_steam_forecast)
        else:
            states_forecast_steam = None
        states_forecast = hmm_obj.model_forecast.predict(X_weather_forecast)
        self.from_date = from_date
        self.to_date = to_date
        self.steam_obj = steam_obj
        self.weather_obj = weather_obj
        self.wobj_forecast = wobj_forecast
        self.sobj_forecast = sobj_forecast
        self.hmm_obj = hmm_obj
        self.states_forecast = states_forecast
        self.states_forecast_steam = states_forecast_steam

    def get_similar_states_dates(self,wdf,inputts,start,end,num):
        '''
        returns the dates (of days) that contain similar state sequence

        Arguments
        ---------
        wdf     : weather data (in pandas.DataFrame format)
        inputts : input time series of state sequence
        start   : start time of the day
        end     : end time of the day
        num     : number of dates to be returned

        Returns
        -------
        dates : in %Y%j format
    
        Parameters
        ----------
        days        : dates in dt.datetime format
        weekdays    : dates in days format

        Examples
        --------

        
        '''
        weekday_name = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
        mywdf = wdf
        wdf = {}
        for x in mywdf.columns:
            if(dt.datetime.strptime(str(int(x)),'%Y%j').weekday() <= 4):
                wdf[x] = mywdf[x]
        mywdf = pd.DataFrame(wdf)
        mywdf = mywdf[(mywdf.index>=start) & (mywdf.index<=end)]
        inputts = inputts[(inputts.index>=start) & (inputts.index<=end)]
        diffdf = mywdf.apply(lambda x:(x==inputts),axis=0).sum()
        diffdf.sort()
        dates = diffdf[-num:].index
        days = [dt.datetime.strptime(str(int(item)),'%Y%j') for item in dates]
        weekdays = [weekday_name[item.weekday()] for item in days ]
        self.days = days
        self.weekdays = weekdays
        return dates

class Data(object):
    '''  
    This is an abstract class that defines a data object

    Arguments
    ---------
    ts  : pandas.TimeSeries object

    Parameters
    ----------
    ts  : pandas.TimeSeries object 

    Methods
    -------
    gen_df  : generate pandas.DataFrame from pandas.TimeSeries

    Examples
    --------
    '''

    def __init__(self,ts=None):
        if len(ts):
            self.ts = ts
        else:
            pass

    def gen_df(self):
        '''
        This method generates a data frame from TimeSeries object of the class

        Examples
        --------

        '''
        ts = self.ts
        hr = pd.Series(ts.index.map(lambda x: x.hour+(float(x.minute)/60)),index=ts.index)
        dod = pd.Series(ts.index.map(lambda x: int('%d%03d'%(x.year,x.dayofyear))),index=ts.index)
        df = pd.concat([ts,dod,hr],axis=1)
        df.columns=['ts','dod','hr']
        df = df.drop_duplicates(cols=['hr','dod'],take_last=True)
        df = df.pivot(columns='dod',index='hr',values='ts')
        self.df = df


class HMM(Data):
    '''
    This class holds data specific to HMM model and also implements methods to process it

    Arguments
    ---------
    n_states    : number of (latent) states in the HMM model
    steam_obj   : an object of Steam class
    weather_obj : an object of Weather class

    Parameters
    ----------
    df_hmm  : Hmm data in pandas.DataFrame format
    X_hmm   : Hmm data as an array

    Methods
    -------
    build_model             : use steam, weather, time of day to create HMM model
    build_forecast_model    : slice the HMM model to create a forecast model
    plot_model              : plot the HMM model created
    plot_elbow              : if n_states is not initialized, use elbow plot to identify number of states
    gen_covariates          : generate covariates for forecasting
    gen_meta_data           : create X_hmm to be fit in HMM
    gen_ts                  : create a pandas.TimeSeries object of hidden states

    Examples
    --------
    '''
    def __init__(self,**kwargs):
        if 'steam_obj' not in kwargs:
            self.steam_obj = Steam()
        else:
            self.steam_obj = kwargs['steam_obj']
        if 'weather_obj' not in kwargs:
            self.weather_obj = Weather()
        else:
            self.weather_obj = kwargs['weather_obj']
        steam_obj = self.steam_obj
        weather_obj = self.weather_obj
        hour_of_day = steam_obj.ts.index.map(lambda x: x.hour + (x.minute/60.0))
        day_of_week = steam_obj.ts.index.map(lambda x: x.dayofweek)
        df_hmm = pd.DataFrame({'steam':steam_obj.ts,'weather':weather_obj.ts, \
                'hour_of_day':hour_of_day,'day_of_week':day_of_week},index=steam_obj.ts.index)
        #its imp that the order for columns is maintain 
        #while slicing the HMM model 
        self.df_hmm,self.X_hmm = self.gen_meta_data(steam_obj,weather_obj) 
        if 'n_states' not in kwargs:
            self.plot_elbow(3,40)
        else:
            self.n_states = kwargs['n_states']

    def __len__(self):
        return len(self.X_hmm)

    def build_model(self):
        n_states = self.n_states
        X_hmm = self.X_hmm
        self.model = GaussianHMM(n_states,covariance_type='diag',n_iter=1000)
        self.model.fit([X_hmm])
        self.hidden_states = self.model.predict(X_hmm)

    def build_forecast_model(self):
        model = self.model
        n_states = self.n_states
        model_forecast = copy.deepcopy(model)
        model_forecast.n_features = model.n_features-1
        model_forecast._means_ = model.means_[:,1:]
        model_forecast._covars_ = model._covars_[:,1:]
        self.model_forecast = model_forecast

    def gen_meta_data(self,steam_obj=None,weather_obj=None):
        if steam_obj!=None:
            hour_of_day = steam_obj.ts.index.map(lambda x: x.hour + (x.minute/60.0))
            day_of_week = steam_obj.ts.index.map(lambda x: x.dayofweek)           
            df_hmm = pd.DataFrame({'steam':steam_obj.ts,'weather':weather_obj.ts, \
                        'hour_of_day':hour_of_day},index=steam_obj.ts.index)
            #df_hmm = pd.DataFrame({'steam':steam_obj.ts,'weather':weather_obj.ts, \
            #            'hour_of_day':hour_of_day,'day_of_week':day_of_week},index=steam_obj.ts.index)
           # X_hmm = df_hmm.as_matrix(columns=['steam','weather'])
            X_hmm = df_hmm.as_matrix(columns=['steam','weather','hour_of_day'])
            #X_hmm = df_hmm.as_matrix(columns=['steam','weather','hour_of_day','day_of_week'])
        else:
            hour_of_day = weather_obj.ts.index.map(lambda x: x.hour + (x.minute/60.0))
            day_of_week = weather_obj.ts.index.map(lambda x: x.dayofweek)           
            df_hmm = pd.DataFrame({'weather':weather_obj.ts, \
                    'hour_of_day':hour_of_day},index=weather_obj.ts.index)
            #df_hmm = pd.DataFrame({'weather':weather_obj.ts, \
            #        'hour_of_day':hour_of_day,'day_of_week':day_of_week},index=weather_obj.ts.index)
           # X_hmm = df_hmm.as_matrix(columns=['weather'])
            X_hmm = df_hmm.as_matrix(columns=['weather','hour_of_day'])
            #X_hmm = df_hmm.as_matrix(columns=['weather','hour_of_day','day_of_week'])
        return df_hmm,X_hmm

    def plot_model(self,x_ax=None,y_ax=None):
        X_hmm = self.X_hmm
        steam_ts = self.steam_obj.ts
        if x_ax == None:
            x_ax = np.asarray([item.to_datetime() for item in steam_ts.index])
        if y_ax == None:
            y_ax = X_hmm[:,0]
        hidden_states = self.hidden_states
        n_states = self.n_states
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for i in xrange(n_states):
            print i
            idx = (hidden_states==i)
            if i<7:
                ax.plot(x_ax[idx],y_ax[idx],'o',label='%dth state'%i)
            elif i<14:
                ax.plot(x_ax[idx],y_ax[idx],'x',label='%dth state'%i)
            elif i<21:
                ax.plot(x_ax[idx],y_ax[idx],'+',label='%dth state'%i)
            elif i<28:
                ax.plot(x_ax[idx],y_ax[idx],'*',label='%dth state'%i)
        ax.set_title('%d State HMM'%(n_states))
        ax.legend()
        ax.set_ylabel('Load (Mlb/Hr)')
        ax.set_xlabel('Time')
        ax.grid(True)
        plt.show()


    def plot_elbow(self,start,end):
        '''
        Fit GMM and plot elbow using AIC & BIC
        '''
        from sklearn.mixture import GMM,DPGMM
        obs = self.X_hmm
        aics = []
        bics = []
        for i in range(start,end+1):
            n_iter=1000
            for j in range(1,11):
                g = GMM(n_components=i,n_iter=n_iter)
                g.fit(obs)
                print i
                converged =  g.converged_
                if converged:
                    print 'j:%d'%(j)
                    break
                n_iter += 1000
            aics.append(g.aic(obs))
            bics.append(g.bic(obs))
        if not converged:
            print 'Not Converged!!'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(range(start,end+1),aics,label='AIC')
        ax.plot(range(start,end+1),bics,label='BIC')
        ax.set_xlabel("No. of Clusters")
        ax.set_ylabel("Information Loss")
        ax.set_xticks(range(start,end+1),minor=True)
        ax.legend()
        ax.grid(True,which='both')
        plt.show()

        def gen_covariates(self):
            hidden_states = self.hidden_states
            self.covariates = pd.DataFrame({'hidden_states':hidden_states},index=self.steam_obj.ts.index)
        def gen_ts(self):
            hidden_states = self.hidden_states
            steam_obj =  self.steam_obj
            self.ts = pd.TimeSeries(hidden_states,index=steam_obj.ts.index)
            

class Steam(Data):
    '''

    Arguments
    ---------
    from_date       : start date of data
    to_date         : end date of data
    data_reader_obj : object of DataReader class

    Parameters
    ----------

    Methods
    -------
    read_data       : call DataReader method
    preprocess_data : perform operations on the data
    gen_df          : generate pandas.DataFrame object for the data
    gen_covariates  : generate covariates for predictor module

    Examples
    --------

   ''' 
    def __init__(self,from_date=None,to_date=dt.date.today(),**keywords):
        self.data_reader_obj = keywords['data_reader_obj']
        self.from_date = from_date
        self.to_date = to_date
        self.data = self.read_data()
        self.preprocess_data()
        self.gen_df()
        self.gen_covariates()

    def __len__(self):
        return len(self.ts)
    
    def read_data(self):
        self.data_reader_obj.read_data()
        return self.data_reader_obj.rows

    def preprocess_data(self):
        data = self.data
        from_date = self.from_date
        to_date = self.to_date
        steam_load = [item[1] for item in data]
        steam_dates = [item[0].replace(second=0,microsecond=0) for item in data]
        steam_df = pd.DataFrame({'load':steam_load,'dates':steam_dates})
        steam_df = steam_df.drop_duplicates(cols='dates',take_last=True)
        ts = pd.TimeSeries(steam_df['load'].tolist(),index=steam_df['dates'])
        dates = pd.DateRange(min(steam_dates),max(steam_dates),offset=pd.DateOffset(minutes=15))
        ts = ts.reindex(dates)
        #TODO Change this to expolation
        self.ts = ts.interpolate() 
        #ts[pd.isnull(ts)] should return empty list
        self.ts=self.ts[from_date:to_date][:-1]

    def gen_df(self):
        super(Steam,self).gen_df()

    def gen_covariates(self):
        ts = self.ts
        prevday_ts = ts.tshift(1,'D')
        prevday_avg = prevday_ts.resample('D',how='mean')
        prevday_avg = prevday_avg.asfreq('15Min',method='pad')
        prevweek_ts = ts.tshift(7,'D')
        #change min_date of all timeseries to the prevweek_ts date
        min_date = max(min(ts.index),min(prevweek_ts.index),min(prevday_ts.index))
        max_date = max(prevday_ts.index)
        ts = ts[min_date:max_date]
        prevday_ts = prevday_ts[min_date:]
        prevday_avg = prevday_avg[min_date:]
        prevweek_ts = prevweek_ts[min_date:]
        hr = pd.Series(ts.index.map(lambda x: x.hour+(float(x.minute)/60)),index=ts.index)
        dod = pd.Series(ts.index.map(lambda x: int('%d%03d'%(x.year,x.dayofyear))),index=ts.index)
        df = pd.concat([ts,dod,hr],axis=1)
        df.columns=['ts','dod','hr']
        df = df.pivot(columns='dod',index='hr',values='ts')
        hour_of_day = prevday_ts.index.map(lambda x: x.hour + (x.minute/60.0))
        day_of_week = prevday_ts.index.map(lambda x: x.dayofweek)
        covariates = pd.DataFrame({'load':ts,'prevday_load':prevday_ts,'prevweek_load':prevweek_ts,'prevday_avg':prevday_avg,'hour_of_day':hour_of_day,'day_of_week':day_of_week},index=prevday_ts.index)
        #Fill na values for columns: load & prevday_avg
        covariates = covariates.fillna(method='pad')
        self.covariates = covariates
        
class Weather(Data):
    '''

    Arguments
    ---------
    from_date       : start date of data
    to_date         : end date of data
    data_reader_obj : object of DataReader class
    forecast        : boolean, whether the object is a weather forecast

    Parameters
    ----------

    Methods
    -------
    read_data       : call DataReader method
    preprocess_data : perform operations on the data
    gen_df          : generate pandas.DataFrame object for the data
    gen_covariates  : generate covariates for predictor module

    Examples
    --------

    '''
    def __init__(self,from_date=None,to_date=dt.date.today(),**keywords):
        #check if weather forecast
        if 'forecast' in keywords:
            self.forecast = keywords['forecast']
        else:
            self.forecast = False

        self.data_reader_obj = keywords['data_reader_obj']
        self.from_date = from_date
        self.to_date = to_date
        self.data = self.read_data(**keywords)
        self.preprocess_data()
        self.gen_df()
        self.gen_covariates()

    def __len__(self):
        return len(self.ts)
    
    def read_data(self,**keywords):
        self.data_reader_obj.read_data()
        return self.data_reader_obj.rows

    def preprocess_data(self):
        data = self.data
        from_date = self.from_date
        to_date = self.to_date
        temps = [float(item[1]) for item in data]
        dewps = [float(item[2]) for item in data]
        #TODO check why replace doesnt work here
        #db_dates = [item[0].replace(second=0,microsecond=0) for item in data]
        db_dates = [item[0] for item in data]
        weather_df = pd.DataFrame({'temps':temps,'dates':db_dates,'dewps':dewps})
        weather_df = weather_df.drop_duplicates(cols='dates',take_last=True)
        dewps_in_K = 273.16 + (weather_df['dewps'] - 32)/1.8
        temps_in_C = (weather_df['temps'] - 32)/1.8
        humidex = temps_in_C + 0.5555*(6.11 *(np.exp(5417.7530*(1/273.16-1/dewps_in_K))) - 10)
        temp_ts = pd.TimeSeries(weather_df['temps' ].tolist(),index=weather_df['dates'])
        dewp_ts = pd.TimeSeries(weather_df['dewps'].tolist(),index=weather_df['dates'])
        weather_ts = pd.TimeSeries(humidex.tolist(),index=weather_df['dates']) 
        dates = pd.DateRange(min(db_dates),max(db_dates),offset=pd.DateOffset(minutes=15))
        weather_ts = weather_ts.reindex(dates)
        #TODO Change this to expolation
        weather_ts[weather_ts>200] = None
        weather_ts = weather_ts.interpolate() 
        #TODO change the method to interpolation
        if self.forecast==False:
            weather_ts = weather_ts.tshift(-6,freq='Min')
        #ts[pd.isnull(ts)] should return empty list
        temp_ts = temp_ts.reindex(dates)
        temp_ts[temp_ts>200] = None
        temp_ts[temp_ts<-100] = None
        temp_ts = temp_ts.interpolate() 
        #TODO change the method to interpolation
        temp_ts = temp_ts.tshift(-6,freq='Min')
        dewp_ts = dewp_ts.reindex(dates)
        dewp_ts[dewp_ts>200] = None
        dewp_ts[dewp_ts<-100] = None
        dewp_ts = dewp_ts.interpolate() 
        #TODO change the method to interpolation
        dewp_ts = dewp_ts.tshift(-6,freq='Min')
        self.ts = weather_ts
        self.ts = self.ts[from_date:to_date][:-1]
        self.temp_ts = temp_ts
        self.temp_ts = self.temp_ts[from_date:to_date][:-1]
        self.dewp_ts = dewp_ts
        self.dewp_ts = self.dewp_ts[from_date:to_date][:-1]
 
    def gen_df(self):
        super(Weather,self).gen_df()

    def gen_covariates(self):
        '''
        method to generate weather covariates
        '''
        #If time series is Humidex, convert it to dataframe
        #If time series is temps and dewps, create a dataframe from the two
        self.covariates = pd.DataFrame({'humidex':self.ts.values},index=self.ts.index) 
