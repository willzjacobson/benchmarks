# coding=utf-8

__author__ = 'ashishgagneja'

import re

import pytz

import benchmarks.occupancy.utils
import benchmarks.utils
import common.utils
import ts_proc.munge
import ts_proc.utils


def _dow_type(dt):
    """
    Find day of week type.
    Type 1: Mondays are different from other weekdays because the
            building was off over the weekend
    Type 2: Tue-Friday are categorized as one type
    Type 3: weekend has it own type

    :param dt: datetime.date
    :return: int in [1, 2, 3]
    """

    dow = dt.isoweekday()

    if dow in [1]: # Monday
        return 1
    elif dow in [2, 3, 4, 5]: # Tue - Fri
        return 2
    else: # weekend
        return 3


def _find_benchmark(base_dt, occ_ts, wetbulb_ts, obs_ts, gran, timezone,
                    debug):
    """
        Find benchmark steam usage for the date base_dt. Benchmark
        steam usage is defined as the steam usage profile from a similar
        weather and occupancy day in the past with the lowest total daily
        steam usage. weather and occupancy forecasts are used to find such
        a day. Benchmark steam usage for any given day can not go up, it can
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

    # get data availability
    elec_avlblty    = benchmarks.utils.get_data_availability_dates(obs_ts, gran)
    occ_avlblty     = benchmarks.utils.get_data_availability_dates(occ_ts, gran)
    wetbulb_avlblty = benchmarks.utils.get_data_availability_dates(wetbulb_ts,
                                                                    gran)
    data_avlblty = occ_avlblty.intersection(elec_avlblty, wetbulb_avlblty)

    # check if all required data is available for base dt
    if base_dt not in data_avlblty:
        raise Exception("insufficient data available for %s" % base_dt)

    # get weather for base_dt
    base_dt_wetbulb = common.utils.get_dt_tseries(base_dt, wetbulb_ts, timezone)

    # find k closest weather days for which steam and occupancy data is
    # available
    dow_type = _dow_type(base_dt)
    sim_wetbulb_days = common.utils.find_similar_profile_days(base_dt_wetbulb,
                                                              dow_type,
                                                              wetbulb_ts,
                                                              7,
                                                              data_avlblty,
                                                              timezone,
                                                              dow_type_fn=
                                                              _dow_type)
    common.utils.debug_msg(debug, "sim days: %s" % str(sim_wetbulb_days))

    # compute occupancy similarity score for the k most similar weather days
    occ_scores = benchmarks.occupancy.utils.score_occ_similarity(base_dt,
                                                                 sim_wetbulb_days,
                                                                 occ_ts,
                                                                 timezone)
    common.utils.debug_msg(debug, occ_scores)
    # find the date with the lowest steam usage
    return benchmarks.utils.find_lowest_auc_day(occ_scores, obs_ts, 2, timezone,
                                                debug)


def process_building(building, host, port, db_name, username, password,
                     source, collection_name, db_name_out,
                     collection_name_out, weather_hist_db,
                     weather_hist_collection, weather_fcst_db,
                     weather_fcst_collection, granularity,
                     base_dt, steam_meter_count, timezone, debug):
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
    :param steam_meter_count: int
        number of steam meters in use
    :param timezone: pytz.timezone
        target timezone or building timezone
    :param debug: bool
        debug flag

    :return:
    """

    gran_int = int(re.findall('\d+', granularity)[0])
    target_tzone = pytz.timezone(timezone)

    # get wetbulb
    wetbulb_ts = benchmarks.utils.get_weather(host, port, username, password,
                                              source,
                                              weather_hist_db,
                                              weather_hist_collection,
                                              weather_fcst_db,
                                              weather_fcst_collection,
                                              granularity)
    wetbulb_ts = wetbulb_ts.tz_convert(target_tzone)
    # wetbulb_ts = todel.interp_tseries(wetbulb_ts, gran_int)
    common.utils.debug_msg(debug, "wetbulb: %s" % wetbulb_ts)

    # get occupancy data
    occ_ts = ts_proc.utils.get_parsed_ts_new_schema(host, port, db_name,
                                                    username, password,
                                                    source, collection_name,
                                                    building,
                                                    'Occupancy',
                                                    'Occupancy')

    # interpolation converts occupancy data to float; convert back to int64
    # occ_ts = todel.interp_tseries(occ_ts, gran_int).astype(numpy.int64)
    # convert to local time
    occ_ts = occ_ts.tz_convert(target_tzone)
    # occ_ts = ts_proc.munge.munge(occ_ts, 100, 2, '1min', granularity).astype(
    #     numpy.int64)
    common.utils.debug_msg(debug, "occupancy: %s" % occ_ts)

    # query steam data
    steam_ts = ts_proc.utils.get_parsed_ts_new_schema(host, port, db_name,
                                                      username, password,
                                                      source, collection_name,
                                                      building, 'TotalInstant',
                                                      None)
    # steam_ts = todel.interp_tseries(steam_ts, gran_int)
    steam_ts = steam_ts.tz_convert(target_tzone)
    common.utils.debug_msg(debug, "steam: %s" % steam_ts)

    # find baseline
    bench_info = _find_benchmark(base_dt, occ_ts, wetbulb_ts, steam_ts,
                                 gran_int, target_tzone, debug)
    bench_dt, bench_auc, bench_incr_auc, bench_usage = bench_info
    common.utils.debug_msg(debug, "bench dt: %s, bench usage: %s, auc: %s" % (
        bench_dt, bench_usage, bench_auc))

    # save results
    if not debug:
        benchmarks.utils.save_benchmark(bench_dt, base_dt, bench_usage,
                                        bench_auc, bench_incr_auc, host, port,
                                        db_name_out, username, password,
                                        source, collection_name_out,
                                        building, 'Steam_Usage',
                                        'benchmark')
