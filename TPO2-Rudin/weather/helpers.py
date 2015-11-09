__author__ = "David Karapetyan"

import pandas as pd
import numpy as np
import config
from urllib.request import urlopen
import json
import codecs
from dateutil.relativedelta import relativedelta
from joblib import Parallel, delayed

stringcols = ['conds', 'wdire']


def _dtype_conv(df=pd.DataFrame(),
                conds_mapping=config.david["weather"]["conds_mapping"],
                wdire_mapping=config.david["weather"]["wdire_mapping"]):
    """
    :param df: DataFrame
    :return: DataFrame
    """
    # next, convert each column to appropriate data type, so that interpolation
    # works properly (will work on type float, but not on generic object

    # fill done different for text vs float columns
    floatcols = df.columns[df.columns.isin(stringcols) == False]
    # convert each column label to appropriate dtype
    for stringcol in stringcols:
        if stringcol in df.columns:
            df[stringcol] = df[stringcol].apply(
                lambda x: str(x) if x != 'N/A' else np.nan)
    for floatcol in floatcols:
        if floatcol in df.columns:
            df[floatcol] = df[floatcol].apply(
                lambda x: float(x) if x != 'N/A' else np.nan)

    # map conditions to uniformly spaced, unique integer values for processing
    # in models, with basic error checking.
    # conds reflects historical conditions, so bottom
    # code will make forecast conds be identical to history conds
    if 'conds' in df.columns:
        df['conds'] = df['conds'].apply(
            lambda x: conds_mapping[x] if x in conds_mapping.keys()
            else np.nan)
    if 'wdire' in df.columns:
        df['wdire'] = df['wdire'].apply(
            lambda x: wdire_mapping[x] if x in wdire_mapping.keys()
            else np.nan)
        df[['conds', 'wdire']].fillna(method="bfill")
    return df


def _history_pull(date=pd.datetime.today(),
                  city=config.david["weather"]["city"],
                  state=config.david["weather"]["state"],
                  account=config.david["weather"]["wund_url"]):
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

    url = account + \
          "%s/q/%s.json" % (date_path, city_path)

    reader = codecs.getreader('utf-8')
    f = urlopen(url)
    parsed_json = json.load(reader(f))
    f.close()
    observations = parsed_json['history']['observations']

    # convert to dataframes for easy presentation and manipulation

    df = pd.DataFrame.from_dict(observations)


    # convert date column to datetimeindex
    dateindex = df.date.apply(
        lambda x: pd.datetime(int(x['year']), int(x['mon']), int(x['mday']),
                              int(x['hour']), int(x['min'])))

    dateindex.name = None
    df = df.set_index(dateindex)

    return df


def history_munge(df, cov, gran):
    # drop what we don't need anymore, and set df index
    # dropping anything with metric system
    dates = ['date', 'utcdate']
    misc = ['icon', 'metar']
    british = ['visi', 'dewpti']
    metric = ['dewptm', 'heatindexm', 'precipm', 'pressurem', 'tempm',
              'vism', 'wgustm',
              'windchillm', 'wspdm']
    df = df.drop(dates + misc + british + metric, axis=1)
    column_trans_dict = {'heatindexi': 'heatindex', 'precipi': 'precip',
                         'pressurei': 'pressure', 'tempi': 'temp',
                         'wgusti': 'wgust',
                         'windchilli': 'windchill', 'wspdi': 'wspd'}
    df = df.rename(columns=column_trans_dict)
    df = _dtype_conv(df)
    # drop what we don't need anymore. Keeping only identified
    # covariates in config
    df = df[df.columns.intersection(cov)]

    # resampling portion
    df = df.resample(gran, how="last")
    df = df.fillna(method="bfill")

    return df


def forecast_munge(df, cov, gran):
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



    # rename to have name mappings of identical entries in historical and
    # forecast dataframes be the same
    column_trans_dict = {'condition': 'conds', 'humidity': 'hum', 'pop': 'rain'}
    df = df.rename(columns=column_trans_dict)

    # then drop what we don't need anymore, and set df index
    df['conds'] = df['wx']
    df = df[df.columns.intersection(cov)]
    df = _dtype_conv(df)

    # resampling portion
    # wunderground history data is 51 minutes on the hour, every hour.
    # wunderground forecast pull is on the hour, every hour.
    # resamples down to top of hour minus granularity minute mark
    # hence, there will be a granularity amount of time gap between
    # forecast and historical data in our database, which is what we want
    # if pd.datetime.today().time().minute > 51:
    #     df = df.resample(gran, how="last")
    # else:
    #     df = df.resample(gran, how="last", loffset="-1H")

    df = df.fillna(method="bfill")
    return df


def _forecast_pull(city=config.david["weather"]["city"],
                   state=config.david["weather"]["state"],
                   account=config.david["weather"]["wund_url"]):
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
    url = account + "hourly/q/%s.json" % city_path
    reader = codecs.getreader('utf-8')
    f = urlopen(url)
    parsed_json = json.load(reader(f))
    f.close()
    df = parsed_json['hourly_forecast']

    # convert to dataframes for easy presentation and manipulation

    df = pd.DataFrame.from_dict(df)
    dateindex = df.FCTTIME.apply(
        lambda x: pd.datetime(int(x['year']), int(x['mon']), int(x['mday']),
                              int(x['hour']), int(x['min'])))
    dateindex.name = None
    df = df.set_index(dateindex)
    return df


def forecast_update(city, state, account, cov, gran=None, munged=False):
    if munged:
        if gran is None:
            raise ValueError("Please supply a resampling granularity")
        return forecast_munge(_forecast_pull(city, state, account), cov, gran)
    else:
        return _forecast_pull(city, state, account)


# helper function for history_update.
def comp(date, city, state, cov, gran=None, munged=True):
    if munged:
        if gran is None:
            raise ValueError("Please supply a resampling granularity")
        return history_munge(_history_pull(date, city, state), cov, gran)
    else:
        return _history_pull(date, city, state)


def history_update(city, state, archive_location, df, cap, parallel, cov,
                   gran=None,
                   munged=False):
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
    parallel: Boolean. Whether to process in parallel
    munged: Boolean. Whether or not to munge wunderground pulled data


    Returns
    -------
    w: dataframe of weather parameters, indexed by hour
    """

    # error handling built in, better than read_hdf
    # will just create store and entry
    # if they don't exist

    store = pd.HDFStore(archive_location)
    if ("/" + df) not in store.keys():
        store[df] = pd.DataFrame()
    weather_data = store[df]
    store.close()

    # start is beginning of day for last entry in weather_data
    # we toss out any times already existing between start and end of
    # day in archive weather_data, in order for concat below to run without
    # indices clashing

    if len(weather_data.index) == 0:
        start = pd.datetime.today().date() - relativedelta(years=4)
    else:
        start = weather_data.index[-1].date()

    end = pd.datetime.today().date()

    interval = pd.date_range(start, end)
    wdata_days_comp = weather_data[:start]

    if parallel:
        frames = Parallel(n_jobs=config.david["parallel"]["processors"])(
            delayed(comp)(date, city, state, cov, gran, munged)
            for date in interval[:cap])
    else:
        frames = [comp(date, city, state, cov, gran, munged) for date in
                  interval[:cap]]

    weather_update = pd.concat(frames)
    archive = pd.concat([wdata_days_comp, weather_update])

    # check for duplicate entries from weather underground, and delete
    # all except one. Unfortunately, drop_duplicates works only for column
    # entries, not timestamp row indices, so...
    archive = archive.reset_index().drop_duplicates('index').set_index(
        'index')

    return archive
