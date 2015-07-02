import statsmodels.tsa.arima_model as arima
from statsmodels.tsa import stattools
from scipy import optimize
import pandas as pd
# custom funcs


# test for stationarity

def stationarity_test( ts ):
    if stattools.adfuller( ts )[1] > 0.05:
        print( "May be non-stationary after taking first lag" )




# function to find optimal ARIMA order

def arima_aic( endog, order ):
    return arima.ARIMA( endog, order ).fit().aic


def optimal_order( ts ):
    return tuple( 
        map( int,
            optimize.brute( lambda x: arima_aic( ts, x ),
                           ranges = ( slice( 0, 2, 1 ),
                                   slice( 0, 2, 1 ),
                                   slice( 0, 2, 1 ) ),
                           finish = None )
            )
    )


def ts_day_pos( ts, day, start, end, freq ):
    temp_ts = ts[ts > 0]
    temp_ts = temp_ts[pd.date_range( start, end, freq )]
    return temp_ts[temp_ts.index.weekday == day]
