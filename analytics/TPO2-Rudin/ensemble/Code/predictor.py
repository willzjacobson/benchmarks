__author__='Vaibhav Bhandari <vb2317@columbia.edu>'
__module__='predictor'

from abc import ABCMeta,abstractmethod
import datetime as dt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

from data_module import HMMCreator
from data_module import Data
from data_module import Steam
from data_module import Weather
import load_data as ld

DEBUG = True
def gen_ts(self):
    hidden_states = self.hidden_states
    steam_obj =  self.steam_obj
    self.ts = pd.TimeSeries(hidden_states,index=steam_obj.ts.index)

def gen_df(self):
    ts = self.ts
    hr = pd.Series(ts.index.map(lambda x: x.hour+(float(x.minute)/60)),index=ts.index)
    dod = pd.Series(ts.index.map(lambda x: int('%d%03d'%(x.year,x.dayofyear))),index=ts.index)
    df = pd.concat([ts,dod,hr],axis=1)
    df.columns=['ts','dod','hr']
    df = df.drop_duplicates(cols=['hr','dod'],take_last=True)
    df = df.pivot(columns='dod',index='hr',values='ts')
    self.df = df

class Model(object):
    __metaclass__=ABCMeta
    '''
    class to generate Predictor Machine Learning Model

    Arguments
    ---------
    Methods
    -------
    train_model     : to be implemented by every subclass, fit the estimator
    test_model      : to be implemented by every subclass, predict the data
    gen_covariates  : combine covariates from data containers/manipulate them
    calc_mape       : calculate mean absolute percent error between actual and predicted values
    calc_rmse       : calculate root mean square error between actual and predicted values

    Parameters
    ----------
    Examples
    --------
    '''
    def __init__(self):
        '''
        initialize Machine Learning Model
        '''
        pass


    @abstractmethod
    def train_model(self):
        print "Training the Model"

    @abstractmethod
    def test_model(self):
        print "Testing the Model"

    @abstractmethod
    def gen_covariates(self):
        print "Generating Covariates"

    def calc_mape(self):
        print "Calculating Mape"
        y_test = self.sobj_forecast.ts.values
        y_predict = self.y_predict
        self.mape = (np.abs(y_test-y_predict)/y_test).sum()/len(y_test)

    def calc_rmse(self):
        print "Calculating RMSE"
        y_test = self.sobj_forecast.ts.values
        y_predict = self.y_predict
        self.rmse = (((y_test-y_predict)**2).sum()/len(y_test))**0.5


class HMMModel(Model):
    '''
    Include latent states in the ensemble to improve accuracy

    Arguments
    ---------
    n_states            : number of states in the HMM model
    from_date           : start date for data
    to_date             : end date for data
    forecast_time_delta : no of days to be predicted
    hmm_obj             : an object of data_module.HMM
    no_of_days          : number of days to train on
    '''
    def __init__(self,n_states,from_date=dt.date(2012,2,1),to_date=dt.date(2013,7,9),forecast_time_delta=1,hmm_obj=None,no_of_days=12):
        '''
        initialize HMM model
        '''
        self.no_of_days = no_of_days
	dr_obj_steam = ld.DataReaderCsvSteam.instantiate()
	dr_obj_weather = ld.DataReaderCsvWeather.instantiate()
	self.steam_obj = Steam(from_date=from_date,to_date=to_date,data_reader_obj=dr_obj_steam)
        self.sobj_forecast = Steam(from_date=to_date,to_date=to_date+dt.timedelta(forecast_time_delta),data_reader_obj=dr_obj_steam)
	self.weather_obj = Weather(from_date=from_date,to_date=to_date,data_reader_obj=dr_obj_weather)
	self.wobj_forecast = Weather(from_date=to_date,to_date=to_date+dt.timedelta(forecast_time_delta),data_reader_obj=dr_obj_weather)
        self.creator_obj = HMMCreator.instantiate(n_states,from_date,to_date,forecast_time_delta,hmm_obj,self.steam_obj,self.weather_obj,self.wobj_forecast)
        self.from_date = from_date
        self.to_date = to_date
        self.hmm_obj = hmm_obj
        self.states_forecast = self.creator_obj.states_forecast

    def gen_covariates(self):
        hmm_obj = self.hmm_obj
        steam_obj = self.steam_obj
        weather_obj = self.weather_obj
        wobj_forecast = self.wobj_forecast
        states_forecast = self.states_forecast
        to_date = self.to_date
        no_of_days = self.no_of_days
        to_date_str = dt.datetime.strftime(to_date,'%m/%d/%Y')
        DEBUG=False
        if DEBUG:
            states_forecast = self.states_forecast_steam
        DEBUG=True
        states_forecast = pd.Series(states_forecast,index=np.arange(0,24,0.25))
        states_ts = pd.Series(hmm_obj.hidden_states,index=steam_obj.ts.index)
        states_obj = Data(states_ts)
        states_obj.gen_df()
        states_df = states_obj.df
        similar_state_dates = self.creator_obj.get_similar_states_dates(states_df,states_forecast,start=6,end=17,num=no_of_days)
        weather_forecast = pd.Series(wobj_forecast.ts.values,index=np.arange(0,24,0.25))
        #Create Steam Covariates
        steam_values = steam_obj.df[similar_state_dates].unstack().values
        start_date = to_date - dt.timedelta(no_of_days)
        dummy_dates = pd.DateRange(start=start_date,periods=len(steam_values),offset='15Min')
        ts = pd.TimeSeries(steam_values,index=dummy_dates)
        prevday_ts = ts.tshift(1,'D')
        prevday_avg = prevday_ts.resample('D',how='mean')
        prevday_avg = prevday_avg.asfreq('15Min',method='pad')
        #       prevweek_ts = ts.tshift(7,'D')
        #change min_date of all timeseries to the prevweek_ts date
        min_date = max(min(ts.index),min(prevday_ts.index))
        max_date = max(prevday_ts.index)
        ts = ts[min_date:max_date]
        prevday_ts = prevday_ts[min_date:]
        prevday_avg = prevday_avg[min_date:]
        #prevweek_ts = prevweek_ts[min_date:]
        hr = pd.Series(ts.index.map(lambda x: x.hour+(float(x.minute)/60)),index=ts.index)
        dod = pd.Series(ts.index.map(lambda x: int('%d%03d'%(x.year,x.dayofyear))),index=ts.index)
        df = pd.concat([ts,dod,hr],axis=1)
        df.columns=['ts','dod','hr']
        df = df.pivot(columns='dod',index='hr',values='ts')
        hour_of_day = prevday_ts.index.map(lambda x: x.hour + (x.minute/60.0))
        day_of_week = prevday_ts.index.map(lambda x: x.dayofweek)
        covariates = pd.DataFrame({'load':ts,'prevday_load':prevday_ts,'prevday_avg':prevday_avg,'hour_of_day':hour_of_day,'day_of_week':day_of_week},index=prevday_ts.index)
        #Fill na values for columns: load & prevday_avg
        steam_covariates = covariates.fillna(method='pad')
        #Create Weather Covariates
        weather_values = weather_obj.df[similar_state_dates].unstack().values
        start_date = to_date - dt.timedelta(no_of_days)
        dummy_dates = pd.DateRange(start=start_date,periods=len(weather_values),offset='15Min')
        wdf = pd.DataFrame({'humidex':weather_values},index=dummy_dates)
        weather_covariates = pd.concat((wdf,wobj_forecast.covariates),axis=0)
        # Create HMM covariates
        gen_ts(hmm_obj)
        gen_df(hmm_obj)
        state_values = hmm_obj.df[similar_state_dates].unstack().values
        start_date = to_date - dt.timedelta(no_of_days)
        dummy_dates = pd.DateRange(start=start_date,periods=len(state_values),offset='15Min')
        sdf = pd.DataFrame({'hidden_states':state_values},index=dummy_dates)
        state_forecast_df = pd.DataFrame({'hidden_states':states_forecast.values},index=wobj_forecast.ts.index)
        state_covariates = pd.concat((sdf,state_forecast_df),axis=0)
        covariates = steam_covariates.join(weather_covariates)
        covariates = covariates.join(state_covariates)
        covariate_names = list(covariates.columns)
        covariate_names.remove('load')
        X = covariates[covariate_names]
        y = covariates['load']
        self.X = X.ix[:-96]
        self.y = y.ix[:-96]
        self.X_test = X.ix[-96:]
        self.y_test = None
        DEBUG=False
        if DEBUG==True:
            #fill y_test for comparison
            self.X_test = self.X.ix[-96:]
            self.y_test = self.y.ix[-96:]
            self.X = self.X.ix[:-96]
            self.y = self.y.ix[:-96]
        DEBUG=True
        self.similar_state_dates = similar_state_dates

    def train_model(self):
        X = self.X
        y = self.y
        regressor = RandomForestRegressor(n_estimators=100,verbose=2,n_jobs=-1)
        regressor.fit(X,y)
        self.regressor = regressor
    
    def test_model(self):
        regressor = self.regressor
        X_test = self.X_test
        y_predict = regressor.predict(X_test)
        self.y_predict = y_predict

    def train_hourly_model(self):
        X = self.X
        y = self.y
        hours = X.index.map(lambda x: x.hour)
        regressors = []
        for i in xrange(24):
            regressor_hourly = RandomForestRegressor(n_estimators=20,verbose=2,n_jobs=-1)
            regressor_hourly.fit(X[hours==i],y[hours==i])
            regressors.append(regressor_hourly)
        self.regressors = regressors

    def test_hourly_model(self):
        X_test = self.X_test
        regressors = self.regressors
        hours = X_test.index.map(lambda x:x.hour)
        y_predict = []
        for i in xrange(24):
            y_predict.append(regressors[i].predict(X_test[hours==i]))
        self.y_predict = np.hstack(y_predict)


class RandomForestModel(Model):
    '''
    train the covariates with a Random Forest ensemble
    '''
    def __init__(self,steam_obj=None,weather_obj=None,wobj_forecast=None):
        self.steam_obj = steam_obj
        self.weather_obj = weather_obj
        self.wobj_forecast = wobj_forecast

    def gen_covariates(self):
        steam_obj = self.steam_obj
        weather_obj = self.weather_obj
        wobj_forecast = self.wobj_forecast
        weather_covariates = pd.concat((weather_obj.covariates,wobj_forecast.covariates),axis=0)
        steam_covariates = steam_obj.covariates
        covariates = steam_covariates.join(weather_covariates)
        covariate_names = list(covariates.columns)
        covariate_names.remove('load')
        X = covariates[covariate_names]
        y = covariates['load']
        if DEBUG:
            X = X.ix[-15000:]
            y = y.ix[-15000:]
        self.X = X.ix[:-96]
        self.y = y.ix[:-96]
        self.X_test = X.ix[-96:]
        self.y_test = None
        if DEBUG==True:
            #fill y_test for comparison
            self.X_test = self.X.ix[-96:]
            self.y_test = self.y.ix[-96:]
            self.X = self.X.ix[:-96]
            self.y = self.y.ix[:-96]

    def train_model(self):
        X = self.X
        y = self.y
        regressor = RandomForestRegressor(n_estimators=20,verbose=2,n_jobs=-1)
        regressor.fit(X,y)
        self.regressor = regressor
    
    def test_model(self):
        regressor = self.regressor
        X_test = self.X_test
        y_predict = regressor.predict(X_test)
        self.y_predict = y_predict

    def train_hourly_model(self):
        X = self.X
        y = self.y
        hours = X.index.map(lambda x: x.hour)
        regressors = []
        for i in xrange(24):
            regressor_hourly = RandomForestRegressor(n_estimators=20,verbose=2,n_jobs=-1)
            regressor_hourly.fit(X[hours==i],y[hours==i])
            regressors.append(regressor_hourly)
        self.regressors = regressors

    def test_hourly_model(self):
        X_test = self.X_test
        regressors = self.regressors
        hours = X_test.index.map(lambda x:x.hour)
        y_predict = []
        for i in xrange(24):
            y_predict.append(regressors[i].predict(X_test[hours==i]))
        self.y_predict = y_predict


def main():
    pass
    
if __name__=='__main__':
    main()
