from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
from scipy.optimize import brute
import pandas as pd


# custom funcs


# test for stationarity

def stationarity_test(ts):
    lower = 0
    upper = 10

    for i in range(lower, upper):
        if adfuller(ts)[1] < 0.05:
            return "Is stationary only after taking at least {} lags".format(str(i))

    print("May not be stationary even after {}-{} lags".format(str(lower), str(upper)))


# function to find optimal ARIMA order

def arima_aic(endog, order):
    return ARIMA(endog, order).fit().aic


def optimal_order(ts):
    return tuple(
        map(int,
            brute(lambda x: arima_aic(ts, x),
                  ranges=(slice(0, 2, 1),
                          slice(0, 2, 1),
                          slice(0, 2, 1)),
                  finish=None)
            )
    )


def ts_day_pos(ts, day, start, end, freq):
    temp_ts = ts[ts > 0]
    temp_ts = temp_ts[pd.date_range(start, end, freq)]
    return temp_ts[temp_ts.index.weekday == day]
