from urllib.request import urlopen
import json
import codecs

import pandas as pd
from dateutil.relativedelta import relativedelta


def weather_day(date=pd.datetime.today(), city="New_York", state="NY"):
    """Pull weather information

    Weather information is pulled from weather underground at specified
    day

    Parameters
    ----------
    date: datetime object
    city: string
    state: string

    Returns
    -------
    w: Dataframe of weather parameters, indexed by hour
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
    observations = observations.resample("60Min", how="last", closed="right",
                                         loffset="60Min")
    observations = observations.fillna(method="pad")
    return observations


def weather_forecast(city="New_York", state="NY"):
    """Returns forecasts from now until end of day

     Parameters
     ----------

     city: string
     state: string

     Returns
     -------

     w: dataframe of weather parameters, indexed by hour
    """

    city_path = '%s/%s' % (state, city)
    url = 'http://api.wunderground.com/' \
          'api/bab4ba5bcbc2dbec/hourly/q/%s.json' % city_path
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
    forecast = forecast.resample("60Min", how="last", closed="right",
                                 loffset="60Min")
    forecast = forecast.fillna(method="pad")
    return forecast


def weather_archive_update(city="New_York", state="NY"):
    """Pull archived weather information

    Weather information is pulled from weather underground from end of
    prescriptive weather database date to today, then added to
    weather database

    Parameters
    ----------
    city: string
    state: string
    start: datetime object
    end: datetime object

    Returns
    -------
    w: dataframe of weather parameters, indexed by hour
    """

    from IPython.parallel import Client

    rc = Client()
    dview = rc[:]
    dview.block = True
    with dview.sync_imports():
        import pandas as pd

    date = pd.datetime.today()
    store_string = "df_munged_resampled"
    store = pd.HDFStore('data/weather_history.h5')
    weather_data = store['df_munged_resampled']
    start = weather_data.index[-1] + relativedelta(hours=1)
    end = pd.datetime.today()
    interval = pd.date_range(start, end)

    frames = dview.map_sync(lambda x: weather_day(x, city, state), interval)
    # archive = dview.map_sync(pd.concat, frames)
    archive = pd.concat(frames, verify_integrity=True)
    rc.close()
    # store = pd.HDFStore('data/weather_history.h5')
    # store['df'] = pd.concat(frames)
    store.close()
    return archive
