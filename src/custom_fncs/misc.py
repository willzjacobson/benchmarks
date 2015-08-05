from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
from scipy.optimize import brute
import pandas as pd
import numpy as np
import statsmodels.tsa.statespace.sarimax as sarimax
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


# custom funcs


# test for stationarity

def stationarity_test(ts, upper=10):
    """Stationarity test for a time series and its lags.

    Identify minimum number of lags needed of an input time series to transform
    it into a stationary time series. Default upper bound is 10 lags.

    :param ts: pandas.core.series.Series
    :param upper: int, default 10
    :return: None
    """
    lower = 0
    for i in range(lower, upper):
        if adfuller(ts)[1] < 0.05:
            return "Is stationary only after taking at least {} lags".format(
                str(i))

    print("May not be stationary even after {}-{} lags".format(str(lower),
                                                               str(upper)))


def optimal_order(ts):
    """Outputs optimal Arima order for an input time series.

    :param ts: pandas.core.series.Series
    :return: tuple
    """

    return tuple(
        map(int,
            brute(lambda x: ARIMA(ts, x).fit().aic,
                  ranges=(slice(0, 2, 1),
                          slice(0, 2, 1),
                          slice(0, 2, 1)),
                  finish=None)
            )
    )


def ts_day_pos(ts, day, start, end, freq):
    """ Returns slice of input time series

    Time series subset consists of points beginning at start,
    terminating at end, and sampled with an input frequency

    :param ts: pandas.core.series.Series
    :param day: int
    :param start: datetime.datetime
    :param end: datetime.datetime
    :param freq: frequency alias
    :return: pandas.core.series.Series
    """
    return ts[np.logical_and(
        ts.index.weekday == day, pd.date_range(start, end, freq))]


def actual_vs_prediction(ts, order=(2, 1, 0), seasonal_order=(2, 2, 0, 96),
                         days=(0, 1, 2, 3, 4, 5, 6)):
    """Plots SARIMA predictions against real values for each weekday.

    :param ts: pandas.core.series.Series
    :param order: tuple
    :param seasonal_order: tuple
    :param days: tuple
    :return: None
    """
    if len(days) > 2:
        ncols = int(np.ceil(len(days) / 2))
        nrows = 2

    else:
        ncols = len(days)
        nrows = 1

    fig, ax = plt.subplots(nrows, ncols, squeeze=False)

    if ncols > len(days) / 2:
        fig.delaxes(
            ax[nrows - 1, ncols - 1])  # one more plot axes than is needed

    fig.suptitle('In-sample Prediction vs Actual')
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                4: 'Friday',
                5: 'Saturday', 6: 'Sunday'}

    for axentry in ax:
        for i, j in zip(range(ncols), days):
            ts_within_day = ts[ts.index.weekday == j]
            fit = sarimax.SARIMAX(ts_within_day, order=order,
                                  seasonal_order=seasonal_order).fit()
            axentry[i].set_title(weekdays[j])
            axentry[i].plot(fit.data.dates, fit.data.endog.flatten(),
                            label='Actual')
            axentry[i].plot(fit.data.dates, fit.predict().flatten(),
                            label='Prediction')
            axentry[i].legend(loc='best')
            axentry[i].set_xlabel('Weekly Readings')
            axentry[i].set_ylabel('Accumulated Steam Usage ')
    plt.show()
