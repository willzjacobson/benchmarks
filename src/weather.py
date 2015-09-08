from urllib.request import urlopen
import json
import codecs

from IPython.parallel import Client
import pandas as pd
from dateutil.relativedelta import relativedelta


def dtype_conv(df, weather_type):
    if weather_type == 'forecast':
        floats = ['hum', 'snow', 'temp', 'windchill', 'wspd', 'wdird']
        strings = ['conds', 'wdire']
    elif weather_type == 'history':
        floats = ['fog', 'hail', 'heatindex', 'hum', 'precip',
                  'pressure', 'rain', 'snow', 'temp', 'thunder', 'tornado',
                  'wdird', 'wgust', 'windchill', 'wspd']
        strings = ['conds', 'wdire']

    else:
        raise ValueError("You must enter in an appropriate weather type")

    # convert each column label to appropriate dtype
    for stringcol in strings:
        df[stringcol] = df[stringcol].apply(
            lambda x: str(x) if x != 'N/A' else 'nan')
    for floatcol in floats:
        df[floatcol] = df[floatcol].apply(
            lambda x: float(x) if x != 'N/A' else 'nan')

    return df


def pull(date=pd.datetime.today(), city="New_York", state="NY"):
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

    return dtype_conv(observations, "history")


def forecast(city="New_York", state="NY"):
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
    df = parsed_json['hourly_forecast']

    # convert to dataframes for easy presentation and manipulation

    df = pd.DataFrame.from_dict(df)

    # toss out metric system in favor of english system

    for column in ['windchill', 'wspd', 'temp', 'qpf', 'snow', 'mslp',
                   'heatindex', 'dewpoint', 'feelslike']:
        df[column] = df[column].apply(
            lambda x: x['english']
        )

        # add columns from forecast data to match weather underground past
        # data pull

        df['wdird'] = df['wdir'].apply(
            lambda x: x['degrees'])
        df['wdire'] = df['wdir'].apply(
            lambda x: x['dir'])

    dateindex = df.FCTTIME.apply(
        lambda x: pd.datetime(int(x['year']), int(x['mon']), int(x['mday']),
                              int(x['hour']), int(x['min'])))
    dateindex.name = None

    # drop what we don't need anymore, and set df index
    df = df.drop(
        ['FCTTIME', 'fctcode', 'feelslike', 'dewpoint', 'pop',
         'icon', 'icon_url',
         'wx', 'wdir', 'uvi', 'mslp', 'qpf', 'sky',
         'heatindex'],
        axis=1)
    column_trans_dict = {'humidity': 'hum', 'condition': 'conds'}
    df = df.rename(columns=column_trans_dict)
    df = df.set_index(dateindex)

    # just need 1 day of forecasts
    df = df[pd.datetime.today().strftime('%Y%m%d')]
    df = df.resample("60Min", how="last", closed="right",
                     loffset="60Min")

    df = dtype_conv(df, "forecast")

    df = df.fillna(method="pad")
    return df


def archive_update(city="New_York", state="NY"):
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

    weather_data = pd.read_hdf('data/weather_history.h5', 'df_munged_resampled')
    start = weather_data.index[-1] + relativedelta(hours=1)
    end = pd.datetime.today()
    interval = pd.date_range(start, end)

    rc = Client()
    dview = rc[:]
    dview.block = True
    frames = dview.map_sync(lambda x: pull(x, city, state), interval)

    [dtype_conv(df, "history") for df in frames]

    weather_update = pd.concat(frames, verify_integrity=True)
    archive = pd.concat([weather_data, weather_update])
    # store = pd.HDFStore('data/weather_history.h5')
    # store['df'] = pd.concat(frames)
    return archive

