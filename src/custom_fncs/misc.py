from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
from scipy.optimize import brute
import numpy as np
import pandas as pd
import scipy as sp
from scipy import amin
from scipy import absolute
import statsmodels.tsa.statespace.sarimax as sarimax
import statsmodels.tsa.stattools as stattools
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
    :return: int
    """
    for i in range(upper):
        if adfuller(ts)[1] < 0.05:
            return "Is stationary only after taking at least {} lags".format(
                str(i))

    raise ValueError(
        "May not be stationary even after {}-{} lags".format(str(lower),
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


def ts_day_pos(ts, day, time, start, end, freq):
    """Returns slice of input time series

    Time series subset consists of points beginning at start,
    terminating at end, and sampled with an input frequency

    :param ts: pandas.core.series.Series
    :param day: int, day of week
    :param time: datetime.datetime, time of day. Defaults to None
    :param start: datetime.datetime
    :param end: datetime.datetime
    :param freq: frequency alias
    :return: pandas.core.series.Series
    """
    temp = ts[pd.date_range(start=start, end=end, freq=freq)]
    temp = temp[temp.index.weekday == day]

    if time == None:
        return temp
    else:
        return temp.at_time(time)


def actual_vs_prediction(ts, order=(2, 1, 0), seasonal_order=(1, 0, 0, 96),
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


def number_ar_terms(ts):
    """ Determine the optimal number of AR terms in a SARIMA time series

    The optimal number of terms is computed via analyzing the partial
    auto-correlations of the input time series.

    :param ts: pandas.core.series.Series
    :return: int
    """

    cap = 10  # once we have a larger cluster, can delete
    array = stattools.pacf(ts)
    for i in range(len(array)):
        if array[i] < 0:
            if i < cap:
                return i - 1

            # lines below can be deleted once we have a bigger cluster
            #
            else:
                mag_array_ratios = absolute((sp.roll(array, -1) / array)[:-1])
                for pos, entry in enumerate(mag_array_ratios):
                    if entry == amin(mag_array_ratios):
                        return pos + 1

    raise ValueError("Time Series is invalid")


def number_diff(ts, upper=10):
    """Number of differencings needed to induce stationarity.

    Identify minimum number of differencings needed of an input time
    series to transform it into a stationary time series.
    Default upper bound is 10 lags.

    :param ts: pandas.core.series.Series
    :param upper: int, default 10
    :return: int
    """
    tuple = adfuller(ts)
    pvalue, ar_lags = tuple[1:3]

    for i in range(upper):
        if pvalue < 0.1:
            return i
        else:
            ts = ts.diff()[1:]
            pvalue = adfuller(ts, usedlag=ar_lags)[1]

    raise ValueError(
        "May not be stationary even after 0-{} lags".format(
            str(upper)))  # adfuller(park_ts_logr[

# park_ts_logr.index.weekday == 7].at_time('11:00'), autolag='AIC')
