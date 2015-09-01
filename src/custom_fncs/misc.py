from urllib.request import urlopen
import json
import codecs

from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
from scipy.optimize import brute
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import pacf
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
import seaborn as sns

sns.set()
from IPython.parallel import Client

rc = Client()
dview = rc[:]
dview.block = True


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

    if time is None:
        return temp
    else:
        return temp.at_time(time)


def filter_two_std(ts):
    stats = ts.describe(percentiles=[.05, .95])
    low, high = stats['5%'], stats['95%']
    return ts[ts.between(low, high)]


def actual_vs_prediction(ts, order=(1, 1, 0), seasonal_order=(1, 1, 0, 96),
                         days=(0, 1, 2, 3, 4, 5, 6)):
    """Plots SARIMA predictions against real values for each weekday.

    :param ts: pandas.core.series.Series
    :param order: tuple
    :param seasonal_order: tuple
    :param days: tuple
    :return: None
    """
    days_length = len(days)
    if days_length > 2:
        nrows = int(np.ceil(days_length / 2))
        ncols = 2

    else:
        ncols = days_length
        nrows = 1

    fig, ax = plt.subplots(nrows, ncols, squeeze=False)

    if nrows * ncols > days_length:
        fig.delaxes(ax[nrows - 1, ncols - 1])  # one more plot than needed

    fig.suptitle('In-sample Prediction vs Actual')
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                4: 'Friday',
                5: 'Saturday', 6: 'Sunday'}
    title = ts.name

    fit_list = dview.map_sync(lambda x:
                              SARIMAX(
                                  ts[ts.index.weekday == x],
                                  order=order,
                                  seasonal_order=seasonal_order).fit(), days)

    fit_dict = {day: fit_list[index] for (index, day) in enumerate(days)}

    days_iter = iter(days)
    day = next(days_iter, None)
    for axrow in ax:
        for i in range(ncols):
            if day is not None:
                fit = fit_dict[day]
                axrow[i].set_title(weekdays[day])
                axrow[i].plot(ts.index, ts.values,
                              label='Actual')
                ts_fit = pd.Series(data=fit.predict().flatten(),
                                   index=fit.data.dates)
                ts_fit_filtered = filter_two_std(ts_fit)
                axrow[i].plot(ts_fit_filtered.index, ts_fit_filtered.values,
                              label='Prediction')
                axrow[i].legend(loc='best')
                axrow[i].set_ylabel(title)
                day = next(days_iter, None)
    plt.show()
    plt.draw()
    plt.tight_layout()  # doesn't work without plt.draw coming before


def number_ar_terms(ts):
    """ Determine the optimal number of AR terms in a SARIMA time series

    The optimal number of terms is computed via analyzing the partial
    auto-correlations of the input time series.

    :param ts: pandas.core.series.Series
    :return: int
    """

    cap = 10  # once we have a larger cluster, can delete
    array = pacf(ts)
    for i in range(len(array)):
        if array[i] < 0:
            if i < cap:
                return i - 1

            # lines below can be deleted once we have a bigger cluster
            #
            else:
                mag_array_ratios = np.absolute((np.roll(array, -1)
                                                / array)[:-1])
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




def weather_day_pull(date, city, state):
    """ Pull weather information

    Weather information is pulled from weather underground at specified
    interval

    :return: pandas.core.series.Series
    """
    date_path = 'history_%s%s%s' % (date.strftime('%Y'),
                                    date.strftime('%m'),
                                    date.strftime('%d'))

    city_path = '%s/%s' % (state, city)
    url = 'http://api.wunderground.com/' \
          'api/bab4ba5bcbc2dbec/%s/q/%s.json' % (date_path, city_path)
    reader = codecs.getreader('utf-8')
    f = urlopen(url)
    parsed_json = json.load(reader(f))
    f.close()
    data_dict = parsed_json['history']['observations'][0]
    # dict stored within singly entry list

    title = "New York, NY Daily Maximum Temperature (F)"
    weather_series = pd.Series(data=[data_dict['maxtempi']],
                               index=[date],
                               name=title)
    return weather_series


def weather_day_df(date, city, state):
    """ Pull weather information

    Weather information is pulled from weather underground at specified
    day

    :param date: Datetime object
    :param city: String
    :param state: String

    :return: Dataframe of weather parameters, indexed by day
    """

    date_path = 'history_%s%s%s' % (date.strftime('%Y'),
                                    date.strftime('%m'),
                                    date.strftime('%d'))

    city_path = '%s/%s' % (state, city)
    url = 'http://api.wunderground.com/' \
          'api/bab4ba5bcbc2dbec/%s/q/%s.json' % (date_path, city_path)
    reader = codecs.getreader('utf-8')
    f = urlopen(url)
    parsed_json = json.load(reader(f))
    f.close()
    observations = parsed_json['history']['observations']

    # convert to dataframes for easy presentation and manipulation

    observations = pd.DataFrame.from_dict(observations)

    # convert date column to datetimeindex
    dateindex = observations.date.apply(
        lambda x: pd.datetime(int(x['year']), int(x['mon']), int(x['mday']),
                              int(x['hour']), int(x['min'])))

    # drop what we don't need anymore, and set df index
    observations = observations.drop(['date', 'utcdate'], axis=1)
    observations = observations.set_index(dateindex)
    return observations


def weather_pull(city, state, years_back):
    """ Pull weather information

    Weather information is pulled from weather underground at specified
    interval

    :param city: String
    :param state: String
    :param years_back: Int
    Specifies number of years back to pull, from today

    :return: Dataframe of weather parameters, indexed by day
    """

    weather_data = pd.read_hdf("data/weather_history.h5", key='df')

    end = pd.datetime.today().strftime('%Y%m%d') + relativedelta(days=1)
    start = weather_data[-1].strftime('%Y%m%d') + relativedelta(days=1)
    interval = pd.date_range(start, end)
    frames = dview.map_sync(lambda x: weather_day_df(x, city, state), interval)
    # store = pd.HDFStore('../data/weather_history_parallel.h5')
    # store['df'] = pd.concat(frames)
    return pd.concat(frames)


def weather_pull_to_tomorrow(city, state):
    fore_end = pd.datetime.today().strftime('%Y%m%d') + relativedelta(days=1)
    fore_start = fore_end

    end = pd.datetime.today().strftime('%Y%m%d')
    start = (pd.datetime.today()
             - relativedelta(years=years_back)).strftime('%Y%m%d')
    interval = pd.date_range(start, end)


def start_time(ts, day, end_time, desired_temp):
    """ Identify optimal start-up time

    Fits a SARIMA model to the input time series, then
    backwards iterates from input end_time and desired_temp to
    determine optimal start-up time.

    :param ts: pandas.core.series.Series
    :param day: int
    Numbers 0-6, denoting "Monday"-"Sunday", respectively
    :param end_time: string (am, pm, or military)
    Specifies time by which building must be at desired_temp
    :param desired_temp: Temperature, in Fahrenheit
    :return: datetime.datetime
    """
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
    ts_rev = ts[::-1]

    start, end = ts.index[0], ts.index[-1]
    weather_data = pd.read_hdf("data/weather_history.h5", key='df')
    weather_data = weather_data.between(start, end)

    endog = ts_rev[ts_rev.index == day]
    mod = SARIMAX(endog,
                  order=(p, d, q),
                  seasonal_order=(sp, sd, sq, ss))
    fit_res = mod.fit()

    # new model with same parameters, but different endog and exog data
    rng = pd.date_range(end.date(), freq='15Min')
    endog_addition = pd.Series()

    exog_new = weather_data.between[start, end - relativedelta(days=1)]

    mod_new = SARIMAX(endog_new, exog_new, order=(p, d, q))
    res = mod_new.filter(np.array(fit_res.params))



    # construct time series with predictions
    ts_rev_fit = pd.Series(data=res.predict().flatten(),
                           index=res.data.dates)

    # ts_rev_fit_filtered = filter_two_std(ts_rev_fit)
