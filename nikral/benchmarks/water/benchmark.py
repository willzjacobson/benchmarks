# coding=utf-8
"""
water benchmark support module
"""

__author__ = 'ashishgagneja'

import re

import pytz

import nikral.shared.utils
import nikral.ts_proc.utils
import nikral.benchmarks.utils


def _find_benchmark(base_dt, occ_ts, wetbulb_ts, obs_ts, gran, timezone,
                    debug, holidays):
    """
        Find benchmark water usage for the date base_dt. Benchmark
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
        total water usage time series
    :param gran: int
        expected frequency of observations and forecast in minutes
    :param debug: bool
        debug flag
    :param holidays: list
        list of holidays

    :return: tuple containing benchmark date and a pandas Series object with
        water usage data from that date
    """

    # get data availability
    water_avlblty = nikral.benchmarks.utils.get_data_availability_dates(obs_ts,
                                                                        gran)
    wetbulb_avlblty = nikral.benchmarks.utils.get_data_availability_dates(
                                                            wetbulb_ts, gran)
    occ_avlblty = nikral.benchmarks.utils.get_data_availability_dates(occ_ts,
                                                                      gran)
    data_avlblty = wetbulb_avlblty.intersection(water_avlblty).intersection(
        occ_avlblty)

    # check if all required data is available for base dt
    if base_dt not in wetbulb_avlblty:
        dt_wbuld_ts = nikral.shared.utils.get_dt_tseries(base_dt, wetbulb_ts,
                                                         timezone)
        nikral.shared.utils.debug_msg(debug, "day wetbulb ts: %s\nsize: %s" % (
            dt_wbuld_ts.to_string(), dt_wbuld_ts.size))
        raise Exception("insufficient data available for %s: <wetbulb:%s>" %
                            (base_dt, base_dt in wetbulb_avlblty))

    # get weather for base_dt
    base_dt_wetbulb = nikral.shared.utils.get_dt_tseries(base_dt, wetbulb_ts,
                                                         timezone)

    # find k closest weather days for which steam and occupancy data is
    # available
    dow_type = nikral.shared.utils.dow_type(base_dt)
    sim_wetbulb_days = nikral.shared.utils.find_similar_profile_days(
        base_dt_wetbulb,
        dow_type,
        wetbulb_ts,
        20,
        data_avlblty,
        timezone)
    nikral.shared.utils.debug_msg(debug, "sim days: %s" % str(sim_wetbulb_days))

    # occupancy data availability
    sim_occ_day = None

    # fall-back occupancy lookup
    if base_dt not in occ_avlblty:
        sim_occ_day = nikral.benchmarks.utils.find_similar_occ_day(base_dt,
                                                            occ_ts, holidays)
        nikral.shared.utils.debug_msg(debug, "sim occ day: %s" % sim_occ_day)
        if not sim_occ_day:
            raise Exception("insufficient data available for %s: occupancy" %
                        base_dt)

    # compute occupancy similarity score for the k most similar weather days
    occ_scores = nikral.benchmarks.utils.score_occ_similarity(
        base_dt if not sim_occ_day else sim_occ_day,
        sim_wetbulb_days,
        occ_ts,
        timezone)
    nikral.shared.utils.debug_msg(debug, occ_scores)

    # find the date with the lowest water usage
    return nikral.benchmarks.utils.find_lowest_usage_day(occ_scores, obs_ts, 5,
                                                         timezone, debug, True)


def process_building(building, host, port, db_name, username, password,
                     source, collection_name, db_name_out,
                     collection_name_out, weather_hist_db,
                     weather_hist_collection, weather_fcst_db,
                     weather_fcst_collection, granularity,
                     base_dt, timezone, meter_count, debug, replicaset):
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
    :param meter_count: int
        number of water meters
    :param debug: bool
        debug flag
    :param replicaset: string
        replicaset for database

    :return:
    """

    gran_int = int(re.findall('\d+', granularity)[0])
    target_tzone = pytz.timezone(timezone)

    # get wetbulb
    wetbulb_ts = nikral.benchmarks.utils.get_weather(host, port, username,
                                                     password,
                                                     source,
                                                     weather_hist_db,
                                                     weather_hist_collection,
                                                     weather_fcst_db,
                                                     weather_fcst_collection,
                                                     granularity)
    wetbulb_ts = wetbulb_ts.tz_convert(target_tzone)
    nikral.shared.utils.debug_msg(debug, "wetbulb: %s" % wetbulb_ts)

    # get occupancy data
    occ_ts = nikral.ts_proc.utils.get_parsed_ts_new_schema(host, port, db_name,
                                                           username, password,
                                                           source,
                                                           collection_name,
                                                           building,
                                                           'Occupancy',
                                                           'Occupancy')
    # convert to local time
    occ_ts = nikral.benchmarks.utils.align_idx(occ_ts, gran_int).tz_convert(
        target_tzone)
    nikral.shared.utils.debug_msg(debug, "occupancy: %s" % occ_ts)

    # get water data
    water_ts = nikral.ts_proc.utils.get_water_ts(host, port, db_name, username,
                                                 password, source,
                                                 collection_name, building,
                                                 meter_count)
    water_ts = nikral.benchmarks.utils.align_idx(water_ts, gran_int)
    water_ts = water_ts.tz_convert(target_tzone)
    nikral.shared.utils.debug_msg(debug, "water: %s" % water_ts)

    # find holidays
    holidays = []
    if wetbulb_ts.size:
        holidays = nikral.benchmarks.utils.gen_holidays(
                        wetbulb_ts.index[0].date(), base_dt, building)
    nikral.shared.utils.debug_msg(debug, "holidays: %s" % holidays)

    # find baseline
    bench_info = _find_benchmark(base_dt, occ_ts, wetbulb_ts, water_ts,
                                 gran_int, target_tzone, debug, holidays)
    bench_dt, bench_auc, bench_incr_auc, bench_usage = bench_info
    nikral.shared.utils.debug_msg(debug,
        "bench dt: %s, bench usage: %s, auc: %s" % (bench_dt, bench_usage,
                                                    bench_auc))

    # save results
    if not debug:
        nikral.benchmarks.utils.save_benchmark(bench_dt, base_dt, bench_usage,
                                               bench_auc, bench_incr_auc, host,
                                               port, db_name_out, username,
                                               password, source,
                                               collection_name_out, building,
                                               'building', 'Water_Usage',
                                               target_tzone, replicaset, "Water Consumption Benchmark", "gallons", "water_consumption")