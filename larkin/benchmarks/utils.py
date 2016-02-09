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

import pandas.tseries.holiday

import larkin.shared.utils
import larkin.weather.mongo
import larkin.weather.wund


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
    hist = larkin.weather.mongo.get_history(
            host, port, source_db, history_db,
            username, password, history_collection)
    hist_munged = (larkin.weather.wund.history_munge(hist, gran))['wetbulb']

    fcst = larkin.weather.mongo.get_forecast(host, port, source_db, forecast_db,
                                             username, password,
                                             forecast_collection)
    fcst_munged = (larkin.weather.wund.forecast_munge(fcst, gran))['wetbulb']

    # concatenate history and forecast into one series; prefer history over
    # forecast, if overlapping
    fcst_only_idx = fcst_munged.index.difference(hist_munged)
    wetbulb_ts = pd.concat([hist_munged, fcst_munged.loc[fcst_only_idx]])

    # this data is already in UTC
    return wetbulb_ts.dropna()


def gen_bmark_readings_list(tseries, incr_auc, base_dt, timezone):
    """
    generate list of readings with each item being a dictionary of the form:
    {"time": <datetime/date/time>, "value": <value>, 'daily': <incr_auc>}
    time's timezone must be UTC

    :param tseries: pandas Series
        time series snippet to
    :param incr_auc: list
        list with incremental auc scores, is assumed to be of the same size as
        tseries
    :param base_dt: datetime.date
        base date or as of date
    :param timezone: pytz.timezone
        target timezone or building timezone
    :return: list of dictionaries
    """
    return [{'time': timezone.normalize(timezone.localize(
        datetime.datetime.combine(base_dt, t[0]))).astimezone(pytz.utc),
             'value': t[1],
             'daily': auc}
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
    return set([key for key, cnt in itertools.ifilterfalse(
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
    Finds the day with the lowest total obs usage from among the n most
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
            day_obs_ts = larkin.shared.utils.get_dt_tseries(dt, obs_ts,
                                                            timezone)

            # compute total and incremental AUC
            datum = day_obs_ts.index[0]
            x = list(map(lambda y: (y - datum).total_seconds() / 3600.0,
                         day_obs_ts.index))
            incr_auc, auc = incremental_trapz(day_obs_ts.values.flatten(), x)
            larkin.shared.utils.debug_msg(debug, "%s, %s" % (dt, auc))

            if 0 < auc < min_usage[1]:
                min_usage = [dt, auc, incr_auc,
                             larkin.shared.utils.drop_series_ix_date(
                                 day_obs_ts)]

    return min_usage


def find_lowest_usage_day(date_scores, obs_ts, n, timezone, debug,
                          drop_first=False):
    """
    Finds the day with the lowest total obs usage from among the n most
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
    :param drop_first: bool
        flag indicating whether to ignore first/midnight observation

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
            day_obs_ts = larkin.shared.utils.get_dt_tseries(dt, obs_ts,
                                                            timezone,
                                                            drop_first)

            # compute total and incremental AUC
            day_obs_data = day_obs_ts.values.flatten()
            incr_auc, auc = day_obs_data, day_obs_data[-1]
            larkin.shared.utils.debug_msg(debug, "%s, %s" % (dt, auc))

            if 0 < auc < min_usage[1]:
                min_usage = [dt, auc, incr_auc,
                             larkin.shared.utils.drop_series_ix_date(
                                 day_obs_ts)]

    return min_usage


def save_benchmark(bench_dt, base_dt, bench_ts, bench_auc, bench_incr_auc,
                   host, port, database, username, password, source_db,
                   collection_name, building, bmark_type, system, timezone):
    """
    Save benchmark time series to database

    :param bench_dt: datetime.date
        date from the past most similar to base date
    :param base_dt: datetime.date
        base date or as of date
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
    :param building: string
        building identifier
    :param bmark_type: string
        bmark_type name for identifying time series
    :param system: string
        field name for identifying time series
    :param timezone: pytz.timezone
        target timezone or building timezone

    :return:
    """

    with pymongo.MongoClient(host, port) as conn:
        conn[database].authenticate(username, password, source=source_db)
        collection = conn[database][collection_name]

        base_dt_t = datetime.datetime.combine(base_dt, datetime.time())
        # delete all existing matching documents
        doc_id = {"building": building,
                  "type"    : bmark_type,
                  "system"  : system,
                  "date"    : base_dt_t}
        collection.remove(doc_id)

        # insert
        doc = { "building": building,
                "type"    : bmark_type,
                "system"  : system,
                "date"    : base_dt_t,
                "comment" : datetime.datetime.combine(bench_dt,
                                                      datetime.time()),
                "readings": gen_bmark_readings_list(bench_ts, bench_incr_auc,
                                                    base_dt, timezone),
                "daily_total": bench_auc}
        collection.insert(doc)


def align_idx(obs_ts, granularity):
    """
    align pandas Series index based on granularity and drop second and
    microsecond data

    :param obs_ts: pandas Series
    :param granularity: int
    :return: pandas Series with re-aligned index
    """
    tmp_ts = obs_ts.reset_index()
    tmp_ts['minute'] = obs_ts.index.minute
    tmp_ts['new_index'] = tmp_ts['index'].apply(
        lambda t: t - datetime.timedelta(seconds=t.second,
                                         microseconds=t.microsecond))
    return tmp_ts[tmp_ts['minute'] % granularity == 0].set_index('new_index'
                                            )[obs_ts.name].tz_localize(pytz.utc)


def gen_holidays(start_dt, end_dt, building):
    """
    generate building-specific list of holidays between start and end dates

    :param start_dt: datetime.date
    :param end_dt: datetime.date
    :param building: string
    :return: list of holidays
    """
    # TODO: if building specific list of holidays is available, use that instead
    print("generating holidays for %s" % building)
    return pandas.tseries.holiday.USFederalHolidayCalendar().holidays(
        start=start_dt, end=end_dt).to_pydatetime()


def is_holiday(dt, holidays):
    """
    check if date is a holiday

    :param dt: datetime.date
    :param holidays: list of holidays
    :return: bool
    """
    return datetime.datetime.combine(dt, datetime.time.min) in holidays


def find_similar_occ_day(base_dt, occ_availability, holidays):
    """
    look back from the base date for a day which is likely to have similar
    occupancy

    :param base_dt: datetime.date
    :param occ_availability: list of dates with available actual occupancy data
    :param holidays: list of building-specific holidays

    :return: datetime.date or None
    """
    base_dow_typ = larkin.shared.utils.dow_type(base_dt)
    base_is_holiday = is_holiday(base_dt, holidays)

    sim_occ_day = None
    one_day = datetime.timedelta(days=1)

    if not base_is_holiday: # non-holiday case

        for i in range(1, 31):

            tmp_dt = base_dt - i * one_day
            if is_holiday(tmp_dt, holidays):
                continue

            if larkin.shared.utils.dow_type(tmp_dt) == base_dow_typ:
                if tmp_dt in occ_availability:
                    sim_occ_day = tmp_dt
                    break

    else: # holiday case

        for i in range(374, 1, -1):
            tmp_dt = base_dt - i * one_day
            if not is_holiday(tmp_dt, holidays):
                continue

            if tmp_dt in occ_availability:
                sim_occ_day = tmp_dt
                break

    return sim_occ_day


def score_occ_similarity(base_dt, date_shortlist, occ_ts, timezone):
    """
    Score occupancy profile similarity between occupancy predicted for base date
    and that observed on the the short list of dates provided

    :param base_dt: datetime.date
        base date or as of date
    :param date_shortlist: list
        short-list of dates to choose from
    :param occ_ts: pandas Series
        occupancy data
    :param timezone: pytz.timezone
        target timezone or building timezone
    :return: list of tuples sorted by score
        each tuple is of the form (<date>, <similarity_score>)
    """

    # occupancy, use actual only
    base_ts = larkin.shared.utils.get_dt_tseries(base_dt, occ_ts, timezone)
    base_ts_nodatetz = larkin.shared.utils.drop_series_ix_date(base_ts)

    scores = []
    for dt_t in date_shortlist:

        score = larkin.shared.utils.compute_profile_similarity_score(
                    base_ts_nodatetz,
                    larkin.shared.utils.drop_series_ix_date(
                        larkin.shared.utils.get_dt_tseries(dt_t, occ_ts,
                                                           timezone)))

        scores.append((dt_t, score))

    scores.sort(key=lambda x: x[1] if x[1] else sys.maxsize)
    return scores