import pandas as pd

from urllib.request import urlopen
import json
import codecs
from joblib import Parallel, delayed
from dateutil.relativedelta import relativedelta


def _dtype_conv(df, weather_type):
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
    # url = 'http://api.wunderground.com/' \
    #       'api/bab4ba5bcbc2dbec/%s/q/%s.json' % (date_path, city_path)

    url = 'http://api.wunderground.com/' \
          'api/08d25f404214f50b/%s/q/%s.json' % (date_path, city_path)

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
    return _dtype_conv(observations, "history")


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
    # url = 'http://api.wunderground.com/' \
    #       'api/08d25f404214f50b/hourly/q/%s.json' % city_path
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

    df = _dtype_conv(df, "forecast")

    df = df.fillna(method="pad")

    return df


def archive_update(city="New_York", state="NY",
                   archive_location='../data/weather.h5', df='history',
                   cap=100000000):
    """Pull archived weather information

    Weather information is pulled from weather underground from end of
    prescriptive weather database date to today, then added to
    weather database

    Parameters
    ----------
    city: string
    state: string
    archive_location: string. Location of HDFS archive on disk
    df: string. Name of weather dataframe in archive_location HDFS store
    cap: int. Cap for number of WUnderground pulls, due to membership
    restrictions


    Returns
    -------
    w: dataframe of weather parameters, indexed by hour
    """
    weather_data = pd.read_hdf(archive_location, df)
    # start is beginning of day for last entry in weather_data
    # we toss out any times already existing between start and end of
    # day in archive weather_data, in order for concat below to run without
    # indices clashing

    if len(weather_data.index) == 0:
        start = pd.datetime.today().date() - relativedelta(years=10)
    else:
        start = weather_data.index[-1].date()

    end = pd.datetime.today()
    interval = pd.date_range(start, end)
    wdata_days_comp = weather_data[:start]

    frames = (Parallel(n_jobs=-1)(delayed(pull)(x, city, state)
                                  for x in interval[:cap]))

    frames = [_dtype_conv(df, "history") for df in frames]

    weather_update = pd.concat(frames)
    archive = pd.concat([wdata_days_comp, weather_update])

    # check for duplicate entries from weather underground, and delete
    # all except one. Unfortunately, drop_duplicates works only for column
    # entries, not timestamp row indices, so...

    return archive.reset_index().drop_duplicates('date').set_index(
        'date')
