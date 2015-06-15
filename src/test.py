import subprocess
import os
import numpy as np
import pandas as pd
import ggplot 
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com
import scipy
from statsmodels.tsa import * 
#load R forecast package
forecast = importr('forecast')


# for wide terminal display of pandas dataframes
pd.options.display.width = 120

# set project working directory
os.chdir( '/users/davidkarapetyan/documents/workspace/data_analysis/' )

# convert dynamodb table to csv
subprocess.call( 'cd /users/davidkarapetyan/node_modules/dynamodbtocsv; \
node dynamodbtocsv.js -t WeMo > \
/users/davidkarapetyan/documents/workspace/data_analysis/data/wemo.csv',
                 shell =True,
                 executable = '/bin/zsh' )


wemo_data = pd.read_csv( 'data/wemo.csv' )
wemo_data = wemo_data.sort( 'name' )
average_power = wemo_data.current_power.mean()


#ditch some entries
wemo_data = wemo_data.loc[:, ['name', 'today_kwh']]

# rename columns
wemo_data.columns = ['timestamp', 'energy_used_kw_hrs']


#construct time series
wemo_data_ts = pd.Series(list(wemo_data.energy_used_kw_hrs),
                    list(wemo_data.timestamp), name="Energy Used (kw_hrs)")


#test for stationarity

if (stattools.adfuller(wemo_data_ts.values)[1] > 0.05):
    print("May be non-stationary after taking first lag")
else:
    print("Most likely stationary after first lag")



def arima_aic(endog, order):
    fit = arima_model.ARIMA(endog, order).fit()
    return fit.aic


from scipy.optimize import brute
grid = (slice(0, 2, 1), slice(0,2,1), slice(0, 2, 1))

optimal_order_wemo = tuple(
                      map(int,
                          brute(lambda x: arima_aic(wemo_data_ts.values, x),
                                grid, finish=None)
                          )
                      )


wemo_data_ts_fit = arima_model.ARIMA(wemo_data_ts.values,
                                     optimal_order_wemo).fit()




##########
#start park data analysis

park_data = pd.read_csv( 'data/park345_steam.csv' )
park_data = park_data.sort( 'TIMESTAMP' )


#ditch some entries
park_data = park_data.loc[park_data.VALUE > 0.01, :]
park_data = park_data.loc[:, ['TIMESTAMP', 'VALUE']]



#construct time series
park_data_ts = pd.Series(list(park_data.VALUE),
                    list(park_data.TIMESTAMP), name="steam values")


#test for stationarity

if (stattools.adfuller(park_data_ts.values)[1] > 0.05):
    print("May be non-stationary after taking first lag")
else:
    print("Most likely stationary after first lag")




optimal_order_park = tuple(
                      map(int,
                          brute(lambda x: arima_aic(park_data_ts.values, x),
                                grid, finish=None)
                          )
                      )


park_data_ts_fit = arima_model.ARIMA(park_data_ts.values,
                                     optimal_order_park).fit()







#best is (0,1,1) (or, equivalently, (1,0,1)



# export to json
#data.to_json( 'data/wemo_munged.json' )


# ggplot(aes(x='timestamp', y='energy_used_kw_hrs'), data=data_ts) + \
# geom_line() + \
# stat_smooth(colour='blue', span=0.2)




