# coding=utf-8

""" Utility functions for benchmarks
"""
import datetime
import itertools

__author__ = 'ashishgagneja'


import pandas as pd

import weather.mongo
import weather.wund


def filter_missing_weather_data(weather_df):
    """
    Filter/remove rows with missing data like -9999's
    :param weather_df: pandas DataFrame
        dataframe with weather data

    :return: pandas DataFrame
    """

    # TODO: it might be better not to ignore good data in records with
    # some missing data
    bad_data = weather_df.where(weather_df < -998).any(axis=1)
    return weather_df.drop(bad_data[bad_data == True].index)



def get_weather(host, port, username, password, source_db, history_db,
                 history_collection, forecast_db, forecast_collection, gran):
    """ Load all available weather data, clean it and drop unneeded columns

    :param host: string
        db_name server name or IP-address
    :param port: int
        db_name port number
    :param username: string
        db_name username
    :param password: string
        db_name password
    :param source_db: string
        source database name for authentication
    :param history_db: string
        database name for historical weather
    :param history_collection: string
        collection name for historical weather
    :param forecast_db: string
        database name for weather forecast
    :param forecast_collection: string
        collection name for weather forecast
    :param gran: string
        sampling frequency of input data and forecast data

    :return: pandas DataFrame
    """

    # TODO: this should be done before munging for efficiency
    hist = weather.mongo.get_history(host, port, source_db, history_db,
                                     username, password, history_collection)
    hist_munged = (weather.wund.history_munge(hist, gran))['wetbulb']

    fcst = weather.mongo.get_latest_forecast(host, port, source_db, forecast_db,
                                             username, password,
                                             forecast_collection)
    fcst_munged = (weather.wund.forecast_munge(fcst, gran))['wetbulb']

    # concatenate history and forecast into one series; prefer history over
    # forecast, if overlapping
    fcst_only_idx = fcst_munged.index.difference(hist_munged)
    wetbulb_ts = pd.concat([hist_munged, fcst_munged.loc[fcst_only_idx]])

    return wetbulb_ts.dropna()



def gen_bmark_readings_list(tseries, incr_auc):
    """
    generate list of readings with each item being a dictionary of the form:
    {"time": <datetime/date/time>, "value": <value>, 'daily': <incr_auc>}

    :param tseries: pandas Series
        time series snippet to
    :param incr_auc: list
        list with incremental auc scores, is assumed to be of the same size as
        tseries
    :return: list of dictionaries
    """

    return [{'time': str(t[0]), 'value': t[1], 'daily': auc}
            for t, auc in zip(tseries.iteritems(), incr_auc)]



def get_data_availability_dates(obs_ts, gran):
    """
    Find the set of dates for which data is available.
    Dates for which < THRESHOLD % data is available are dropped.

    Assumption: Series has no NA's
    Assumption: THRESHOLD := 85

    :param obs_ts: pandas Series
        time series object
    :param gran: int
        sampling frequency of input data and forecast data
    :return: set
    """

    ts_list = list(map(datetime.datetime.date, obs_ts.index))
    counts = [[key, len(list(grp))] for key, grp in itertools.groupby(ts_list)]

    thresh = 0.85 * 24 * 60 / gran
    return set([key for key, cnt in itertools.filterfalse(
        lambda x: x[1] < thresh, counts)])



def incremental_trapz(y, x):
    """
    compute area under the curve incrementally

    :param y: list
        list of y co-ordinates
    :param x: list
        list of  co-ordinates

    :return: tuple
        (<list of incremental AUCs>, <total auc>)
        the length of the list of incremental AUCs matches that of y
    """

    if len(y) != len(x):
        raise Exception('length of x and y must match')

    incr_auc, curr_total = [], 0.0
    for i, y_i in enumerate(y):

        if i > 0:
            curr_total += (y_i + y[i - 1]) * (x[i] - x[i - 1]) / 2.0
        incr_auc.append(curr_total)

    return incr_auc, curr_total