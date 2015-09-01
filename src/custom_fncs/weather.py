from urllib.request import urlopen
import json
import codecs

from statsmodels.tsa.arima_model import ARIMA
from scipy.optimize import brute
import pandas as pd
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
    # dropping anything with metric system
    dates = ['date', 'utcdate']
    misc = ['icon', 'metar']
    british = ['visi', 'dewpti']
    metric = ['dewptm', 'heatindexm', 'precipm', 'pressurem', 'tempm',
              'vism', 'wgustm',
              'windchillm', 'wspdm']
    observations = observations.drop(dates + misc + british + metric, axis=1)
    column_trans_dict = {'heatindexi': 'heatindex', 'precipi': 'precip',
                         'pressurei': 'pressure', 'tempi': 'temp',
                         'wgusti': 'wgust',
                         'windchilli': 'windchill', 'wspdi': 'wspd'}
    observations = observations.rename(columns=column_trans_dict)
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


def weather_pull_forecast(city, state):
    city_path = '%s/%s' % (state, city)
    url = 'http://api.wunderground.com/' \
          'api/bab4ba5bcbc2dbec/hourly/q/%s.json' % (city_path)
    reader = codecs.getreader('utf-8')
    f = urlopen(url)
    parsed_json = json.load(reader(f))
    f.close()
    forecast = parsed_json['hourly_forecast']

    # convert to dataframes for easy presentation and manipulation

    forecast = pd.DataFrame.from_dict(forecast)

    # toss out metric system in favor of english system

    for column in ['windchill', 'wspd', 'temp', 'qpf', 'snow', 'mslp',
                   'heatindex', 'dewpoint', 'feelslike']:
        forecast[column] = forecast[column].apply(
            lambda x: x['english']
        )

        # add columns from forecast data to match weather underground past
        # data pull

        forecast['wdird'] = forecast['wdir'].apply(
            lambda x: x['degrees'])
        forecast['wdire'] = forecast['wdir'].apply(
            lambda x: x['dir'])

    dateindex = forecast.FCTTIME.apply(
        lambda x: pd.datetime(int(x['year']), int(x['mon']), int(x['mday']),
                              int(x['hour']), int(x['min'])))
    dateindex.name = None

    # drop what we don't need anymore, and set df index
    forecast = forecast.drop(
        ['FCTTIME', 'fctcode', 'feelslike', 'dewpoint', 'pop',
         'icon', 'icon_url',
         'wx', 'wdir', 'uvi', 'mslp', 'qpf', 'sky',
         'heatindex'],
        axis=1)
    column_trans_dict = {'humidity': 'hum', 'condition': 'conds'}
    forecast = forecast.rename(columns=column_trans_dict)
    forecast = forecast.set_index(dateindex)

    # just need 1 day of forecasts
    forecast = forecast[pd.datetime.today().strftime('%Y%m%d')]
    return forecast
