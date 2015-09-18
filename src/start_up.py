import numpy as np
import statsmodels.tsa.statespace.sarimax
import statsmodels.tsa.stattools
import pandas as pd
from dateutil.relativedelta import relativedelta


def number_ar_terms(ts):
    """ Determine the optimal number of AR terms in a SARIMA time series

    The optimal number of terms is computed via analyzing the partial
    auto-correlations of the input time series.

    :param ts: pandas.core.series.Series
    :return: int
    """

    cap = 10  # once we have a larger cluster, can delete
    array = statsmodels.tsa.stattools.pacf(ts)
    for i in range(len(array)):
        if array[i] < 0:
            if i < cap:
                return i - 1

            # lines below can be deleted once we have a bigger cluster
            #
            else:
                mag_array_ratios = np.absolute(
                    (np.roll(array, -1) / array)[:-1])
                for pos, entry in enumerate(mag_array_ratios):
                    if entry == np.amin(mag_array_ratios):
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
    my_tuple = statsmodels.tsa.stattools.adfuller(ts)
    pvalue, ar_lags = my_tuple[1:3]

    for i in range(upper):
        if pvalue < 0.1:
            return i
        else:
            ts = ts.diff()[1:]
            pvalue = statsmodels.tsa.stattools.adfuller(ts, maxlag=ar_lags)[1]

    raise ValueError(
        "May not be stationary even after 0-{} lags".format(
            str(upper)))  # statsmodels.tsa.stattools.adfuller(park_ts_logr[


# park_ts_logr.index.weekday == 7].at_time('11:00'), autolag='AIC')


# def predict_start_time(ts, crit_time = '7:00:00'):

def benchmark_ts(ts, datetime):
    """ Identify benchmark time series to feet to start_up module

    Parameters
    ----------

    ts: pandas.core.series.Series
    datetime: string
    temp_range: tuple

    Returns
    -------

    w: pandas.core.series.Series
    """

    seasons = {"spring": (3, 6), "summer": (6, 9), "fall": (9, 12),
               "winter": (12, 3)}

    datetime = pd.to_datetime(datetime)
    month = datetime.month
    month_range = (0, 0)

    for value in seasons.values():
        if value[0] < month <= value[1]:
            month_range = value

    # filter by day and season
    ts_filt = []
    for temp_range in [(70, 72), (68, 74), (66, 76), (64, 78), (62, 80)]:
        ts_filt = ts[((ts.index.weekday == datetime.weekday()) &
                      (ts < temp_range[1]) &
                      (ts > temp_range[0]) &
                      (ts.index.month > month_range[0]) &
                      (ts.index.month <= month_range[1])
                      )]

        # check that we have a complete time series
        if len(ts_filt.at_time('00:00:00')) == 0:
            continue

    if len(ts_filt) == 0:
        raise ValueError("Complete benchmark Time Series could not be found for"
                         " indicated temperature ranges")



    # filter by benchmark day given by taking min over
    #  all values at input time

    benchmark_date = ts_filt.at_time(datetime.time()).argmin().date()
    return ts_filt[ts_filt.index.date == benchmark_date]


def start_time(ts, city="New_York", state="NY",
               date="2013-06-06 7:00:00"):
    """ Identify optimal start-up time

    Fits a SARIMA model to the input time series, then
    backwards iterates from input end_time and desired_temp to
    determine optimal start-up time.

    :param ts: pandas.core.series.Series
    Numbers 0-6, denoting "Monday"-"Sunday", respectively
    Specifies time by which building must be at desired_temp
    :return: datetime.datetime
    """
    date = pd.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    freq = ts.index.freqstr

    if freq is None:
        raise ValueError("Time Series is missing frequency attribute")

    periods = len(pd.date_range('1/1/2011', '1/2/2011', freq=freq)) - 1

    p = number_ar_terms(ts)
    d = number_diff(ts)
    q = 0

    sp = p
    sd = d
    sq = q
    ss = periods

    # weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
    #             4: 'Friday',
    #             5: 'Saturday', 6: 'Sunday'}

    # reverse the time series
    # ts = ts[::-1]

    # start, end = ts.index[0], ts.index[-1]
    # weather.data = pd.read_hdf("data/weather.history.h5",
    #                            key='df_munged_resampled')

    endog_temp = ts[(ts.index.weekday == date.weekday()) &
                    (ts.index.date < date.date())]

    weather_history = pd.read_hdf(
        '../data/weather_history.h5', 'df_munged_resampled')

    forecast = pd.read_hdf('../data/weather_history.h5', 'forecast')

    weather_all = pd.concat([weather_history, forecast])

    wtemp = weather_all.temp.resample(freq).interpolate()
    intsec = wtemp.index.intersection(endog_temp.index)

    endog = endog_temp.loc[intsec]
    exog = wtemp.loc[intsec]

    # resample exog

    mod = statsmodels.tsa.statespace.sarimax.SARIMAX(endog=endog[::-1],
                                                     exog=exog[::-1],
                                                     order=(p, d, q),
                                                     seasonal_order=(
                                                         sp, sd, sq, ss),
                                                     enforce_stationarity=False)
    fit_res = mod.fit()

    # new model with same parameters, but different endog and exog data
    start = (endog.index[-1] + relativedelta(weeks=1)).date()
    end = start + relativedelta(days=1)

    # rng should not include 00:00:00 time in next day
    rng = pd.date_range(start, end, freq='15Min')[:-1]
    benchmark_data = list(benchmark_ts(ts, datetime=date).values)
    endog_addition = pd.Series(index=rng, data=benchmark_data)

    # create new endog variable by filling day for prediction
    # post 7:00am values with benchmark ts values

    endog_new_temp = pd.concat([endog, endog_addition])
    intsec_new = wtemp.index.intersection(endog_new_temp.index)

    endog_new = endog_new_temp.loc[intsec_new]
    exog_new = wtemp.loc[intsec_new]

    # create model object, and replace ar/ma coefficients
    # with those from previous fitted model on larger sample of data

    mod_new = statsmodels.tsa.statespace.sarimax.SARIMAX(
        endog_new[::-1],
        exog_new[::-1],
        order=(p, d, q),
        seasonal_order=(
            sp, sd, sq, ss),
        enforce_stationarity=False)
    res = mod_new.filter(np.array(fit_res.params))

    # moment of truth: prediction
    # find offset by counting backwards from end of day to system cutoff
    # time we wish to forecast backwards from

    offset = endog_new[date:].shape[0] - 1
    prediction = res.predict(dynamic=offset, full_results=True)
    predict = prediction.forecasts

    # # construct time series with predictions. Have to drop first p terms,
    # as first p terms are needed to forecast forward
    ts_fit = pd.Series(data=predict.flatten()[p:],
                       index=res.data.dates[p:])

    return ts_fit
