import pickle
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from predictor import HMMModel
from data_module import Data

def predict_rf_hmm_choose_n():
    results_df = pd.DataFrame()
    js = []
    rmses = []
    for i in [1,2,3,4,9,10,11,12]:
        hmm_obj = pickle.load(open('hmm_23_201304%02d.pickle'%i))
        from_date = dt.date(2012,1,2)
        to_date = dt.date(2013,4,i)
        min_rmse = 9999
        for j in range(5,21):
            hmm = HMMModel(23,from_date,to_date,hmm_obj=hmm_obj,no_of_days=j)
            hmm.gen_covariates()
            hmm.train_model()
            hmm.test_model()
            hmm.calc_rmse()
            if hmm.rmse<min_rmse:
                min_rmse = hmm.rmse
                y_predict = hmm.y_predict
                min_j = j
        rmses.append(min_rmse)
        js.append(min_j)
        result_df = pd.DataFrame({'y_test':hmm.sobj_forecast.ts.values,'y_predict':y_predict},index=hmm.sobj_forecast.ts.index)
        results_df = pd.concat((results_df,result_df))
    pd.DataFrame({'RMSE':rmses,'No Of Days':js}).to_csv('../Output/April_ens_rf_hmm_statecovs_nchoose_rmse.csv')
    results_df.to_csv('../Output/April_ens_rf_hmm_statecovs_nchoose.csv')

def predict_rf_hmm():
    results_df = pd.DataFrame()
    for i in [1,2,3,4,9,10,11,12]:
        hmm_obj = pickle.load(open('hmm_23_201304%02d.pickle'%i))
        from_date = dt.date(2012,1,2)
        to_date = dt.date(2013,4,i)
        hmm = HMMModel(23,from_date,to_date,hmm_obj=hmm_obj)
        hmm.gen_covariates()
        hmm.train_model()
        hmm.test_model()
        result_df = pd.DataFrame({'y_test':hmm.sobj_forecast.ts.values,'y_predict':hmm.y_predict},index=hmm.sobj_forecast.ts.index)
        results_df = pd.concat((results_df,result_df))
    results_df.to_csv('../Output1/April_ens_rf_hmm_statecovs.csv')

def predict_rf_hmm_hourly():
    results_df = pd.DataFrame()
    for i in [1,2,3,4,9,10,11,12]:
        hmm_obj = pickle.load(open('hmm_23_201304%02d.pickle'%i))
        from_date = dt.date(2012,1,2)
        to_date = dt.date(2013,4,i)
        hmm = HMMModel(23,from_date,to_date,hmm_obj=hmm_obj,no_of_days=12)
        hmm.gen_covariates()
        hmm.train_hourly_model()
        hmm.test_hourly_model()
        y_predict = np.hstack(hmm.y_predict)
        result_df = pd.DataFrame({'y_test':hmm.sobj_forecast.ts.values,'y_predict':y_predict},index=hmm.sobj_forecast.ts.index)
        results_df = pd.concat((results_df,result_df))
    results_df.to_csv('../Output/April_ens_rf_hmm_hourly_statecovs.csv')

def plot_results_from_files_actual(filenames=[],titles=[]):

    def format_date(x,pos=None):
        N=len(df)
        thisind = np.clip(int(x+0.5),0,N-1)
        return pd.Timestamp(df.index.values[thisind]).to_datetime().strftime('%Y-%m-%d')

    rmses_list = []
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig2=plt.figure()
    ax_error = fig2.add_subplot(212)
    ax.set_title('Steam Load Demand')
    for i,filename in enumerate(filenames):
        print filename
        #fig = plt.figure()
        df = pd.read_csv(filename)
        df_index = df[df.columns[0]].astype('datetime64[ns]')
        df.index = df_index
        if i==0:
            ax.plot(df['y_test'].values)
            ax.grid(True)
            ax.set_xlabel('TIME')
            ax.set_ylabel('STEAM Mlb/Hr')
            dates = ['2013-04-%02d'%item for item in [1,2,3,4,9,10,11,12]]
            ax_error.set_xticklabels(dates,rotation=30)
            ax_error.grid(True)
            ax_error.set_xlabel('TIME')
            ax_error.set_ylabel('RMSE')         
            ax_error.plot(np.zeros(8))
        #ax.plot(df['y_predict'].values)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        fig.autofmt_xdate()
        rmse_iter = calc_rmse(df,dates)
        rmses = [x for x in rmse_iter]
        rmses_list.append(rmses)
        ax_error.plot(rmses)
    rmses_df = pd.DataFrame(rmses_list).T
    ax_error.plot(rmses_df.min(axis=1).values,linewidth=2)
    ax.legend(['Actual','Model 1','SVR TPO1','Model 2','Model 3','Model 4'],loc='upper left')
    ax_error.legend(['Actual','Model 1','SVR TPO1','Model 2','Model 3','Model 4','Best Model Ensemble'],loc='upper left')
    plt.show()


def plot_results_from_files(filenames=[],titles=[]):

    def format_date(x,pos=None):
        N=len(df)
        thisind = np.clip(int(x+0.5),0,N-1)
        return pd.Timestamp(df.index.values[thisind]).to_datetime().strftime('%Y-%m-%d')

    rmses_list = []
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax_error = fig.add_subplot(212)
    ax.set_title('Predicton & Error Plot')
    for i,filename in enumerate(filenames):
        print filename
        #fig = plt.figure()
        df = pd.read_csv(filename)
        df_index = df[df.columns[0]].astype('datetime64[ns]')
        df.index = df_index
        if i==0:
            ax.plot(df['y_test'].values)
            ax.grid(True)
            ax.set_xlabel('TIME')
            ax.set_ylabel('STEAM Mlb/Hr')
            dates = ['2013-04-%02d'%item for item in [1,2,3,4,9,10,11,12]]
            ax_error.set_xticklabels(dates,rotation=30)
            ax_error.grid(True)
            ax_error.set_xlabel('TIME')
            ax_error.set_ylabel('RMSE')         
            ax_error.plot(np.zeros(8))
        ax.plot(df['y_predict'].values)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        fig.autofmt_xdate()
        rmse_iter = calc_rmse(df,dates)
        rmses = [x for x in rmse_iter]
        rmses_list.append(rmses)
        ax_error.plot(rmses)
    rmses_df = pd.DataFrame(rmses_list).T
    ax_error.plot(rmses_df.min(axis=1).values,linewidth=2)
    ax.legend(['Actual','Model 1','SVR TPO1','Model 2','Model 3','Model 4'],loc='upper left')
    ax_error.legend(['Actual','Model 1','SVR TPO1','Model 2','Model 3','Model 4','Best Model Ensemble'],loc='upper left')
    plt.show()

def plot_results_from_file(filenames=[],titles=[]):

    def format_date(x,pos=None):
        N=len(df)
        thisind = np.clip(int(x+0.5),0,N-1)
        return pd.Timestamp(df.index.values[thisind]).to_datetime().strftime('%Y-%m-%d')

    for i,filename in enumerate(filenames):
        print filename
        fig = plt.figure()
        ax = fig.add_subplot(211)
        df = pd.read_csv(filename)
        df_index = df[df.columns[0]].astype('datetime64[ns]')
        df.index = df_index
        ax.plot(df['y_predict'].values,color='red')
        ax.plot(df['y_test'].values,color='blue')
        ax.set_title(titles[i])
        ax.set_xlabel('TIME')
        ax.set_ylabel('STEAM Mlb/Hr')
        ax.legend(df.columns.values[1:])
        ax.grid(True)
        N = len(df)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        fig.autofmt_xdate()
        ax_error = fig.add_subplot(212)
        dates = ['2013-04-%02d'%item for item in [1,2,3,4,9,10,11,12]]
        rmse_iter = calc_rmse(df,dates)
        rmses = [x for x in rmse_iter]
        ax_error.plot(rmses)
        ax_error.set_xticklabels(dates,rotation=30)
        ax_error.grid(True)
        ax_error.set_xlabel('TIME')
        ax_error.set_ylabel('RMSE')
    plt.show()

def calc_mape(df,dates):
     for date in dates:
        y_test = df['y_test'][date]
        y_predict = df['y_predict'][date]
        yield (np.abs(y_test-y_predict)/y_test).sum()/len(y_test)
    
def calc_rmse(df,dates):
    #print "Calculating RMSE"
    for date in dates:
        y_test = df['y_test'][date]
        y_predict = df['y_predict'][date]
        yield (((y_test-y_predict)**2).sum()/len(y_test))**0.5
        

if __name__=='__main__':
    predict_rf_hmm()
