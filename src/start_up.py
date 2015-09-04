from IPython.parallel import Client

rc = Client()
dview = rc[:]
dview.block = True

with dview.sync_imports():
    from dateutil.relativedelta import relativedelta
    from statsmodels.tsa.stattools import adfuller
    import numpy as np
    import statsmodels.tsa.statespace.sarimax.SARIMAX
    import statsmodels.tsa.stattools
    import weather
    import pandas as pd


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
    my_tuple = adfuller(ts)
    pvalue, ar_lags = my_tuple[1:3]

    for i in range(upper):
        if pvalue < 0.1:
            return i
        else:
            ts = ts.diff()[1:]
            pvalue = adfuller(ts, maxlag=ar_lags)[1]

    raise ValueError(
        "May not be stationary even after 0-{} lags".format(
            str(upper)))  # adfuller(park_ts_logr[


# park_ts_logr.index.weekday == 7].at_time('11:00'), autolag='AIC')


# def predict_start_time(ts, crit_time = '7:00:00'):


def start_time(ts, city="New_York", state="NY",
               date="2014-04-06 7:00:00", desired_temp=72):
    """ Identify optimal start-up time

    Fits a SARIMA model to the input time series, then
    backwards iterates from input end_time and desired_temp to
    determine optimal start-up time.

    :param ts: pandas.core.series.Series
    Numbers 0-6, denoting "Monday"-"Sunday", respectively
    Specifies time by which building must be at desired_temp
    :param desired_temp: Temperature, in Fahrenheit
    :return: datetime.datetime
    """
    date = pd.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    freq = ts.index.freqstr
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

    endog_temp = ts[ts.index.weekday == date.weekday()]
    weather_all = pd.concat([
        weather.archive_update(city, state), weather.forecast(city, state)])
    intsec = weather_all.intersection(endog_temp.index)

    endog = endog_temp[intsec]
    exog = weather_all[intsec]

    mod = statsmodels.tsa.statespace.sarimax.SARIMAX(endog=endog[::-1],
                                                     exog=exog[::-1],
                                                     order=(p, d, q),
                                                     seasonal_order=(
                                                         sp, sd, sq, ss))
    fit_res = mod.fit()

    # new model with same parameters, but different endog and exog data

    rng = pd.date_range(date, date + relativedelta(days=1), freq='15Min')
    endog_addition = pd.Series(index=rng).fillna(desired_temp)

    endog_new_temp = pd.concat([endog, endog_addition])
    intsec_new = weather_all.intersection(endog_new_temp)

    endog_new = endog_new_temp[intsec_new]
    exog_new = weather_all[intsec_new]

    mod_new = statsmodels.tsa.statespace.sarimax.SARIMAX(endog_new[::-1],
                                                         exog_new[::-1],
                                                         order=(p, d, q))
    res = mod_new.filter(np.array(fit_res.params))

    # moment of truth: prediction

    offset = endog_new[::-1][:date].shape[0]
    prediction = res.predict(dynamic=offset, full_results=True)
    predict = prediction.forecasts

    # # construct time series with predictions
    # ts_fit = pd.Series(data=res.predict().flatten(),
    #                    index=res.data.dates)

    return predict
