import subprocess
import os
import pandas as pd
from scipy.optimize import brute
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
# load R forecast package
# import rpy2.robjects as ro
# import pandas.rpy.common as com
# from rpy2.robjects.packages import importr
# forecast = importr( 'forecast' )


# for wide terminal display of pandas dataframes
pd.options.display.width = 120

# set project working directory
os.chdir( '/users/davidkarapetyan/documents/workspace/data_analysis/' )

# convert dynamodb table to csv
subprocess.call( 'cd /users/davidkarapetyan/node_modules/dynamodbtocsv; \
node dynamodbtocsv.js -t WeMo > \
/users/davidkarapetyan/documents/workspace/data_analysis/data/wemo.csv',
                 shell = True,
                 executable = '/bin/zsh' )


wemo_data = pd.read_csv( 'data/wemo.csv' )
wemo_data = wemo_data.sort( 'name' )


# ditch some entries
wemo_data = wemo_data.loc[:, ['name', 'today_kwh']]

# rename columns
wemo_data.columns = ['timestamp', 'energy_used_kw_hrs']


# construct time series
wemo_ts = pd.Series( list( wemo_data.energy_used_kw_hrs ),
                    list( wemo_data.timestamp ), name = "Energy Used (kw_hrs)" )


# test for stationarity
if ( adfuller( wemo_ts )[1] > 0.05 ):
    print( "May be non-stationary after taking first lag" )
else:
    print( "Most likely stationary after first lag" )



def arima_aic( endog, order ):
    fit = ARIMA( endog, order ).fit()
    return fit.aic


grid = ( slice( 0, 2, 1 ), slice( 0, 2, 1 ), slice( 0, 2, 1 ) )

optimal_order_wemo = tuple( 
                      map( int,
                          brute( lambda x: arima_aic( wemo_ts, x ),
                                grid, finish = None )
                          )
                      )


wemo_ts_fit = ARIMA( wemo_ts, optimal_order_wemo ).fit()




##########
# start park data analysis

park_data = pd.read_csv( 'data/park345_steam.csv' )
park_data = park_data.sort( 'TIMESTAMP' )


# ditch some entries
park_data = park_data.loc[park_data.VALUE > 0.01, :]
park_data = park_data.loc[:, ['TIMESTAMP', 'VALUE']]



# construct time series, getting rid of microseconds
temp = pd.Series( list( park_data.VALUE ),
                    pd.DatetimeIndex( park_data.TIMESTAMP ),
                    name = "steam values" )

park_ts = temp.resample( '15Min ', fill_method = 'pad' )





# test for stationarity

if ( adfuller( park_ts )[1] > 0.05 ):
    print( "May be non-stationary after taking first lag" )
else:
    print( "Most likely stationary after first lag" )




optimal_order_park = tuple( 
                      map( int,
                          brute( lambda x: arima_aic( park_ts, x ),
                                grid, finish = None )
                          )
                      )


park_ts_fit = ARIMA( park_ts, optimal_order_park ).fit()


park_ts_fit


# best is (0,1,1) (or, equivalently, (1,0,1)



# export to json
# data.to_json( 'data/wemo_munged.json' )


# ggplot(aes(x='timestamp', y='energy_used_kw_hrs'), data=data_ts) + \
# geom_line() + \
# stat_smooth(colour='blue', span=0.2)




