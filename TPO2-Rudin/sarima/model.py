import numpy as np
import statsmodels.tsa.statespace.sarimax
import statsmodels.tsa.ar_model
import statsmodels.tsa.stattools
import pandas as pd
import ts_proc.munge
from dateutil.relativedelta import relativedelta


# from rpy2.robjects.packages import importr
# import rpy2.robjects as robjects

def _number_ar_terms(ts):
    """ Determine the optimal number of AR terms in a SARIMA time series

    The optimal number of terms is computed via analyzing the partial
    auto-correlations of the input time series.

    :param ts: pandas.core.series.Series
    :return: int
    """
    mod = statsmodels.tsa.ar_model.AR(ts)
    return mod.select_order(maxlag=10, ic="aic")


def _number_diff(ts, upper=10):
    """Number of differencings needed to induce stationarity.

    Identify minimum number of differencings needed of an input time
    series to transform it into a stationary time series.
    Default upper bound is 10 lags.

    :param ts: pandas.core.series.Series
    :param upper: int, default 10
    :return: int
    """
    my_tuple = statsmodels.tsa.stattools.adfuller(ts)
    pvalue, ar_lags = my_tuple[1:3]

    for i in range(upper):
        if pvalue < 0.1:
            return i
        else:
            ts = ts.diff()[1:]
            pvalue = statsmodels.tsa.stattools.adfuller(ts, maxlag=ar_lags)[1]

    raise ValueError("May not be stationary even after 0-{} lags".format(
        str(upper)))


def _benchmark_ts(ts, date_time):
    """ Identify benchmark time series to feet to start_up module

    Parameters
    ----------

    ts: pandas.core.series.Series
    date_time: string
    temp_range: tuple

    Returns
    -------

    w: pandas.core.series.Series
    # """

    ts_filt = ts_proc.munge.filter_day_season(ts, day=date_time.weekday,
                                                    month=date_time.month)  # check that we have a complete time series
    if len(ts_filt.at_time('00:00:00')) != 0:
        raise ValueError("Start of day time missing. Complete benchmark Time"
                         "Series could not be found")

    if len(ts_filt) == 0:
        raise ValueError("Complete benchmark Time Series could not be found for"
                         " indicated temperature ranges")

    # filter by benchmark day given by taking min over
    #  all values at input time

    benchmark_date = ts_filt.at_time(date_time.time()).argmin().date()
    return ts_filt[ts_filt.index.date == benchmark_date]


def start_time(ts, h5file_name, history_name, forecast_name, order,
               enforce_stationarity, granularity, date="2013-06-06 7:00:00"):
    """ Identify optimal start-up time

    Fits a SARIMA model to the input time series, then
    backwards iterates from input end_time and desired_temp to
    determine optimal start-up time.

    :param ts: pandas.core.series.Series
    Numbers 0-6, denoting "Monday"-"Sunday", respectively
    Specifies time by which building_id must be at desired_temp

    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file

    :param order: string
        order params tuple as string for SARIMA model
    :param enforce_stationarity: boolean
        whether to enforce stationarity in the SARIMA model

    :param granularity: int
    sampling frequency of input data and forecast data

    :return: datetime.datetime
    """
    date = pd.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    freq = ts.index.freqstr

    if freq is None:
        raise ValueError("Time Series is missing frequency attribute")

    # periods = len(pd.date_range('1/1/2011', '1/2/2011', freq=freq)) - 1

    # p = _number_ar_terms(ts)
    # d = _number_diff(ts)

    # p = 1
    # d = 1
    # q = 0

    # sp = p
    # sd = d
    # sq = q
    # ss = 4

    # weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
    #             4: 'Friday',
    #             5: 'Saturday', 6: 'Sunday'}

    # reverse the time series
    # ts = ts[::-1]

    # start, end = ts.index[0], ts.index[-1]
    # weather.data = pd.read_hdf("data/weather.history.h5",
    #                            key='history')

    endog_temp = ts[ts.index.date < date.date()]

    weather = pd.read_hdf(h5file_name, history_name)

    forecast = pd.read_hdf(h5file_name, forecast_name)

    weather_all = pd.concat([weather, forecast])

    wtemp = weather_all.temp.resample(freq).interpolate()
    intsec = wtemp.index.intersection(endog_temp.index)

    endog = endog_temp[intsec]
    exog = wtemp[intsec]

    # resample exog

    sarima_order = tuple(map(int, order[1:-1].split(',')))
    mod = statsmodels.tsa.statespace.sarimax.SARIMAX(endog=endog,
                                                     exog=exog,
                                                     order=sarima_order,
                                                     enforce_stationarity=
                                                     enforce_stationarity)
    fit_res = mod.fit()

    # new model with same parameters, but different endog and exog data
    start = (endog.index[-1]).date() + relativedelta(days=1)
    end = start + relativedelta(days=1)

    # rng should not include 00:00:00 time in next day
    rng = pd.date_range(start, end, freq="%dMin" % granularity)[:-1]
    endog_addition = pd.Series(index=rng)

    # create new endog variable by filling day for prediction
    # post 7:00am values with benchmark ts values

    endog_new_temp = pd.concat([endog, endog_addition])
    intsec_new = wtemp.index.intersection(endog_new_temp.index)

    # align indices of endog_new and exog_new, otherwise
    # model will break, thanks Chad Fulton

    endog_new = endog_new_temp[intsec_new]
    exog_new = wtemp[intsec_new]

    # create model object, and replace ar/ma coefficients
    # with those from previous fitted model on larger sample of data

    mod_new = statsmodels.tsa.statespace.sarimax.SARIMAX(
        endog_new,
        exog_new,
        order=sarima_order,
        enforce_stationarity=enforce_stationarity)
    res = mod_new.filter(np.array(fit_res.params))

    # moment of truth: prediction
    # find offset by counting backwards from end of day to system cutoff
    # time we wish to forecast backwards from

    offset = endog.shape[0] - 1
    prediction = res.predict(dynamic=offset, full_results=True)
    # predict = prediction.forecasts

    # # construct time series with predictions. Have to drop first p terms,
    # as first p terms are needed to forecast forward
    # ts_fit = pd.Series(data=predict.flatten()[p:],
    #                    index=res.data.dates[p:])

    return prediction
