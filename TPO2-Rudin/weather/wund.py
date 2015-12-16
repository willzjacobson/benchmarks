# coding=utf-8
import codecs
import json
from urllib.request import urlopen

import numpy as np
import pandas as pd

import config
import weather.wet_bulb

__author__ = "David Karapetyan"

stringcols = ['conds', 'wdire']


def _dtype_conv(df=pd.DataFrame(),
                conds_mapping=config.david["building_dbs"]["conds_mapping"],
                wdire_mapping=config.david["building_dbs"]["wdire_mapping"]):
    """Relabeling of weather underground columns, and conversion of column
    entries to either float or string data types (forecasting models expect
    float entries to have a type signature of 'float')

    :param df: DataFrame
    :param conds_mapping: Dictionary
    Maps original weather underground labels to user-specified labels.
    Used to make weather underground forecast labels match historical data
    labels
    :return: DataFrame
    """
    # next, convert each column to appropriate data type, so that interpolation
    # works properly (will work on type float, but not on generic object

    # fill done different for text vs float columns
    floatcols = df.columns[df.columns.isin(stringcols) == False]
    # convert each column label to appropriate dtype. Convert sentinels
    # (negative numbers) to nan
    for stringcol in stringcols:
        if stringcol in df.columns:
            df[stringcol] = df[stringcol].apply(
                    lambda x: str(x) if x != 'N/A' else np.nan)
    for floatcol in floatcols:
        if floatcol in df.columns:
            df[floatcol] = df[floatcol].apply(
                    lambda x: float(x) if x != 'N/A' and float(
                            x) > -999 else np.nan)

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
        df[['conds', 'wdire']] = df[['conds', 'wdire']].fillna(method="bfill")
    return df


def history_pull(city, state, account, date=pd.datetime.today()):
    """Weather information is pulled from weather underground at specified
    day

    :param date: datetime object
    Date to pull data for
    :param city: string
    City to pull data for
    :param account: string
    Weather underground account url (with key)
    :param state: string
    State to pull data for
    :return: dataframe
    Weather parameters, indexed by hour
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
    observations = parsed_json['weather_history_loc']['observations']

    # convert to dataframes for easy presentation and manipulation

    df = pd.DataFrame.from_dict(observations)

    # convert date column to datetimeindex
    dateindex = df.date.apply(
            lambda x: pd.datetime(int(x['year']), int(x['mon']), int(x['mday']),
                                  int(x['hour']), int(x['min'])))

    dateindex.name = None
    df = df.set_index(dateindex)

    return df


def history_munge(df, gran):
    """For munging history pull from weather underground

    :param df: dataframe
    Weather underground history pull
    :param gran: int
    Resampling granularity
    :return: dataframe
    """
    # drop what we don't need anymore, and set df index
    # dropping anything with metric system
    dates = ['date', 'utcdate']
    misc = ['icon', 'metar']
    metric = ['dewptm', 'heatindexm', 'precipm', 'pressurem', 'tempm',
              'vism', 'wgustm',
              'windchillm', 'wspdm']
    df = df.drop(dates + misc + metric, axis=1)
    column_trans_dict = {'heatindexi': 'heatindex', 'precipi': 'precip',
                         'pressurei': 'pressure', 'tempi': 'temp',
                         'wgusti': 'wgust',
                         'windchilli': 'windchill', 'wspdi': 'wspd',
                         'visi': 'vis', 'dewpti': 'dewpt'}
    df = df.rename(columns=column_trans_dict)
    df = _dtype_conv(df)

    # resampling portion
    df = df.resample(gran, how="last")
    df = df.fillna(method="bfill")

    # add wetbulb temperature
    df['wetbulb'] = df.apply(
            lambda x: weather.wet_bulb.compute_bulb(
                    temp=x['temp'],
                    dewpt=x['dewpt'],
                    pressure=x['pressure']),
            axis=1)

    return df


def forecast_pull(city, state, account):
    """Returns forecasts from now until end of day

     :param city: string
     City portion of city-state pair to pull from weather underground
     :param state: string
     State portion of city-state pair to pull from weather underground
     :return: dataframe of weather parameters, indexed by hour
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


def forecast_munge(df, gran):
    """For munging forecast pull from weather underground

    :param df: dataframe
    Weather underground forecast pull
    :param gran: int
    Resampling granularity
    :return: dataframe
    """
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
    column_trans_dict = {'condition': 'conds', 'humidity': 'hum',
                         'mslp': 'pressure', 'pop': 'rain',
                         'dewpoint': 'dewpt'}
    df = df.rename(columns=column_trans_dict)

    # delete redundant columns
    df['conds'] = df['wx']
    df = df.drop(['wx', 'wdir', 'FCTTIME', 'icon', 'icon_url'], axis=1)

    # appropriate data type conversion for columns
    df = _dtype_conv(df)

    # resampling portion

    df = df.resample(gran, how="last")
    df = df.fillna(method="bfill")

    # add wetbulb temperature
    df['wetbulb'] = df.apply(
            lambda x: weather.wet_bulb.compute_bulb(
                    temp=x['temp'],
                    dewpt=x['dewpt'],
                    pressure=x['pressure']), axis=1)
    return df
