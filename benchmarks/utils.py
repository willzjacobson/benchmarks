# coding=utf-8

""" Utility functions for benchmarks
"""

__author__ = 'ashishgagneja'

import datetime
import itertools
import sys

import pandas as pd
import pymongo
import pytz

import weather.mongo
import weather.wund


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

    fcst = weather.mongo.get_forecast(host, port, source_db, forecast_db,
                                      username, password,
                                      forecast_collection)
    fcst_munged = (weather.wund.forecast_munge(fcst, gran))['wetbulb']

    # concatenate history and forecast into one series; prefer history over
    # forecast, if overlapping
    fcst_only_idx = fcst_munged.index.difference(hist_munged)
    wetbulb_ts = pd.concat([hist_munged, fcst_munged.loc[fcst_only_idx]])

    return wetbulb_ts.dropna().tz_localize(pytz.utc)



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



def find_lowest_auc_day(date_scores, obs_ts, n, timezone, debug):
    """
    Finds the day with the lowest total electric usage from among the n most
    similar occupancy days

    Assumption: Linear interpolation is a reasonable way to fill gaps

    :param date_scores: tuple of tuples
        Each tuple is datetime.date followed by its L2 norm score compared to
        the occupancy forecast for the base date
    :param obs_ts: pandas Series
        Total electric demand time series
    :param n: int
        number of most similar occupancy days to consider
    :param timezone: pytz.timezone
        target timezone or building timezone
    :param debug: bool
        debug flag

    :return: tuple with benchmark date and pandas Series object with usage data
        from benchmark date
    """

    dates, sim_scores = zip(*date_scores)

    if not len(dates):
        return None

    min_usage = [dates[0], sys.maxsize, None, None]
    for i, dt in enumerate(dates):

        if i >= n:
            break

        score = sim_scores[i]
        if score:

            # compute day electric usage by integrating the curve
            day_obs_ts = common.utils.drop_series_ix_date(
                common.utils.get_dt_tseries(dt, obs_ts, timezone))

            # compute total and incremental AUC
            x = list(map(lambda y: y.hour + y.minute / 60.0 + y.second / 3600.0,
                         day_obs_ts.index))
            incr_auc, auc = incremental_trapz(day_obs_ts.data.tolist(), x)
            common.utils.debug_msg(debug, "%s, %s" % (dt, auc))

            if 0 < auc < min_usage[1]:
                min_usage = [dt, auc, incr_auc, day_obs_ts]

    return min_usage



def save_benchmark(bench_dt, base_dt, bench_ts, bench_auc, bench_incr_auc,
                    host, port, database, username, password, source_db,
                    collection_name, bldg_id, system, output_type):
    """
    Save benchmark time series to database

    :param bench_dt: datetime.date
        date from the past most similar to base date
    :param base_dt: datetime.date
        base date
    :param bench_ts: pandas Series
        observation time series from bench_dt
    :param bench_auc: float
        full day's area under the curve as observed on bench_dt
    :param bench_incr_auc: list
        list with incremental auc scores, is assumed to be of the same size as
        bench_ts
    :param host: string
        database server name or IP-address
    :param port: int
        database port number
    :param database: string
        name of the database on server
    :param username: string
        database username
    :param password: string
        database password
    :param source_db: string
        source database for authentication
    :param collection_name: string
        collection name to use
    :param bldg_id: string
        building identifier
    :param system: string
        system name for identifying time series
    :param output_type: string
        field name for identifying time series

    :return:
    """

    with pymongo.MongoClient(host, port) as conn:
        conn[database].authenticate(username, password, source=source_db)
        collection = conn[database][collection_name]

        # delete all existing matching documents
        doc_id = {"_id.building": bldg_id,
                  "_id.system": system,
                  "_id.type": output_type,
                  "_id.date": base_dt.isoformat()}
        collection.remove(doc_id)

        # insert
        doc = {"_id": {"building": bldg_id,
                       "system": system,
                       "type": output_type,
                       "date": base_dt.isoformat()
                       },
               "comment": bench_dt.isoformat(),
               "readings": gen_bmark_readings_list(bench_ts, bench_incr_auc),
               'daily_total': bench_auc}
        collection.insert(doc)



