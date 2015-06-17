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


def arima_aic( endog, order ):
    fit = ARIMA( endog, order ).fit()
    return fit.aic

optimal_order_park = tuple( 
                      map( int,
                          brute( lambda x: arima_aic( park_ts, x ),
                                ranges = ( slice( 0, 2, 1 ),
                                slice( 0, 2, 1 ),
                                slice( 0, 2, 1 ) ),
                                finish = None )
                          )
                      )


park_ts_fit = ARIMA( park_ts, optimal_order_park ).fit()




# best is (0,1,1) (or, equivalently, (1,0,1)



# export to json
# data.to_json( 'data/wemo_munged.json' )


# ggplot(aes(x='timestamp', y='energy_used_kw_hrs'), data=data_ts) + \
# geom_line() + \
# stat_smooth(colour='blue', span=0.2)


