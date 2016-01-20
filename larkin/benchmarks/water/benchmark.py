# coding=utf-8
"""
water benchmark support module
"""

__author__ = 'ashishgagneja'

import re

import pytz

import larkin.shared.utils
import larkin.ts_proc.utils
import larkin.benchmarks.utils


def _find_benchmark(base_dt, occ_ts, wetbulb_ts, obs_ts, gran, timezone,
                    debug):
    """
        Find benchmark steam usage for the date base_dt. Benchmark
        water usage is defined as the water usage profile from a similar
        weather and occupancy day in the past with the lowest total daily
        water usage. weather and occupancy forecasts are used to find such
        a day. Benchmark water usage for any given day can not go up, it can
        only go down as the building operation becomes more efficient

    :param base_dt:
    :param occ_ts: pandas Series
        occupancy time series
    :param wetbulb_ts: pandas Series
        wet bulb time series
    :param obs_ts: pandas Series
        total usage time series
    :param gran: int
        expected frequency of observations and forecast in minutes
    :param debug: bool
        debug flag

    :return: tuple containing benchmark date and a pandas Series object with
        steam usage data from that date
    """
    for arg in [base_dt, occ_ts, wetbulb_ts, obs_ts, gran, timezone, debug]:
        print(arg)
    return None, None, None, None


def process_building(building, host, port, db_name, username, password,
                     source, collection_name, db_name_out,
                     collection_name_out, weather_hist_db,
                     weather_hist_collection, weather_fcst_db,
                     weather_fcst_collection, granularity,
                     base_dt, timezone, debug):
    """ Find baseline steam usage for building

    :param building: string
        building identifier
    :param host: string
        db_name server name or IP-address
    :param port: int
        db_name port number
    :param db_name: string
        name of the db_name on server
    :param username: string
        db_name username
    :param password: string
        db_name password
    :param source: string
        source db_name for authentication
    :param collection_name: string
        name of collection in the db_name
    :param db_name_out: string
        name of the output db_name on server
    :param collection_name_out: string
        name of output collection in the db_name
    :param weather_hist_db: string
        database name for historical weather
    :param weather_hist_collection: string
        collection name for historical weather
    :param weather_fcst_db: string
        database name for weather forecast
    :param weather_fcst_collection: string
        collection name for weather forecast
    :param granularity: string
        expected frequency of observations and forecast
    :param base_dt: datetime.date
        date for which benchmark usage is to be found
    :param timezone: pytz.timezone
        target timezone or building timezone
    :param debug: bool
        debug flag

    :return:
    """

    gran_int = int(re.findall('\d+', granularity)[0])
    target_tzone = pytz.timezone(timezone)

    # get wetbulb
    wetbulb_ts = larkin.benchmarks.utils.get_weather(host, port, username,
                                                     password,
                                                     source,
                                                     weather_hist_db,
                                                     weather_hist_collection,
                                                     weather_fcst_db,
                                                     weather_fcst_collection,
                                                     granularity)
    wetbulb_ts = wetbulb_ts.tz_convert(target_tzone)
    larkin.shared.utils.debug_msg(debug, "wetbulb: %s" % wetbulb_ts)

    # get occupancy data
    occ_ts = larkin.ts_proc.utils.get_parsed_ts_new_schema(host, port, db_name,
                                                           username, password,
                                                           source,
                                                           collection_name,
                                                           building,
                                                           'Occupancy',
                                                           'Occupancy')

    # convert to local time
    occ_ts = occ_ts.tz_convert(target_tzone)
    larkin.shared.utils.debug_msg(debug, "occupancy: %s" % occ_ts)

    # get water data
    water_ts = larkin.ts_proc.utils.get_parsed_ts_new_schema(host, port,
                                                             db_name, username,
                                                             password, source,
                                                             collection_name,
                                                             building,
                                                             'TotalInstant')
    water_ts = water_ts.tz_convert(target_tzone)
    larkin.shared.utils.debug_msg(debug, "water: %s" % water_ts)

    # find baseline
    bench_info = _find_benchmark(base_dt, occ_ts, wetbulb_ts, water_ts,
                                 gran_int, target_tzone, debug)
    bench_dt, bench_auc, bench_incr_auc, bench_usage = bench_info
    larkin.shared.utils.debug_msg(debug,
        "bench dt: %s, bench usage: %s, auc: %s" % (bench_dt, bench_usage,
                                                    bench_auc))

    print("%s:%s" % (db_name_out, collection_name_out))