# coding=utf-8


__author__ = 'ashishgagneja'

import datetime
import itertools
import sys
import re

import pymongo

import common.utils
import ts_proc.utils
import ts_proc.munge
import occupancy.utils
import weather.wet_bulb
import weather.mongo
import weather.wund
import benchmarks.utils


def _get_data_availability_dates(obs_ts, gran):
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

    thresh = 0.85 * 24 * 60 / int(re.findall('\d+', gran)[0])
    return set([key for key, cnt in itertools.filterfalse(
        lambda x: x[1] < thresh, counts)])


def _get_wetbulb_ts(weather_df):
    """
    Compute wet bulb temperature time series from weather data

    :param weather_df: pandas DataFrame
    :return: pandas
    """
    return weather_df.apply(weather.wet_bulb.compute_bulb_helper, axis=1)


def _incremental_trapz(y, x):
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


def find_lowest_electric_usage(date_scores, electric_ts, n, debug):
    """
    Finds the day with the lowest total electric usage from among the n most
    similar occupancy days

    :param date_scores: tuple of tuples
        Each tuple is datetime.date followed by its L2 norm score compared to
        the occupancy forecast for the base date
    :param electric_ts: pandas Series
        Total electric demand time series
    :param n: int
        number of most similar occupancy days to consider
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
            # Assumption: Linear interpolation is a reasonable way to fill gaps
            day_elec_ts = common.utils.drop_series_ix_date(
                common.utils.get_dt_tseries(dt, electric_ts))

            # compute total and incremental AUC
            x = list(map(lambda y: y.hour + y.minute / 60.0 + y.second / 3600.0,
                         day_elec_ts.index))
            incr_auc, auc = _incremental_trapz(day_elec_ts.data.tolist(), x)
            # auc = numpy.trapz(day_elec_ts.data, x=list(map(lambda x:
            # x.hour * 3600
            # + x.minute * 60
            # + x.second,
            #   day_elec_ts.index)))
            common.utils.debug_msg(debug, "%s, %s" % (dt, auc))

            if 0 < auc < min_usage[1]:
                min_usage = [dt, auc, incr_auc, day_elec_ts]

    return min_usage


def _save_benchmark(bench_dt, base_dt, bench_ts, bench_auc, bench_incr_auc,
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
    :param bench_incr_auc: list
        list with incremental auc scores, is assumed to be of the same size as
        bench_ts
    ::param host: string
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
               "readings": _gen_bmark_readings_list(bench_ts, bench_incr_auc),
               'daily_total': bench_auc}
        collection.insert(doc)


def _gen_bmark_readings_list(tseries, incr_auc):
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


def _find_benchmark(base_dt, occ_ts, wetbulb_ts, electric_ts, gran, debug):
    """
        Find benchmark electric usage for the date base_dt. Benchmark
        electric usage is defined as the electric usage profile from a similar
        weather and occupancy day in the past with the lowest total daily
        electric usage. weather and occupancy forecasts are used to find such
        a day. Benchmark electric usage for any given day can not go up, it can
        only go down as the building operation becomes more efficient

    :param base_dt:
    :param occ_ts: pandas Series
        occupancy time series
    :param wetbulb_ts: pandas Series
        wet bulb time series
    :param electric_ts: pandas Series
        total electric usage time series
    :param gran: int
        expected frequency of observations and forecast in minutes
    :param debug: bool
        debug flag

    :return: tuple containing benchmark date and a pandas Series object with
        electric usage data from that date
    """

    # get data availability
    elec_avlblty = _get_data_availability_dates(electric_ts, gran)
    occ_avlblty = _get_data_availability_dates(occ_ts, gran)
    wetbulb_avlblty = _get_data_availability_dates(wetbulb_ts, gran)
    data_avlblty = occ_avlblty.intersection(elec_avlblty, wetbulb_avlblty)

    # check if all required data is available for base dt
    if base_dt not in data_avlblty:
        raise Exception("insufficient data available for %s" % base_dt)

    # get weather for base_dt
    base_dt_wetbulb = common.utils.get_dt_tseries(base_dt, wetbulb_ts)

    # find k closest weather days for which electric and occupancy data is
    # available
    dow_type = common.utils.dow_type(base_dt)
    sim_wetbulb_days = common.utils.find_similar_profile_days(base_dt_wetbulb,
                                                              dow_type,
                                                              wetbulb_ts,
                                                              20,
                                                              data_avlblty)
    common.utils.debug_msg(debug, "sim days: %s" % str(sim_wetbulb_days))

    # compute occupancy similarity score for the k most similar weather days
    occ_scores = occupancy.utils.score_occ_similarity(base_dt, sim_wetbulb_days,
                                                      occ_ts)
    common.utils.debug_msg(debug, occ_scores)
    # find the date with the lowest electric usage
    return find_lowest_electric_usage(occ_scores, electric_ts, 5, debug)


def process_building(building_id, host, port, db_name, username, password,
                     source, collection_name, db_name_out,
                     collection_name_out, weather_hist_db,
                     weather_hist_collection, weather_fcst_db,
                     weather_fcst_collection, granularity,
                     base_dt, debug):
    """ Find baseline electric usage for building_id

    :param building_id: string
        building_id identifier
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
    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file
    :param granularity: string
        expected frequency of observations and forecast
    :param base_dt: datetime.date
        date for which benchmark electric usage is to be found
    :param debug: bool
        debug flag

    :return:
    """

    # get wetbulb
    wetbulb_ts = benchmarks.utils.get_weather(host, port, username, password,
                                              source,
                                              weather_hist_db,
                                              weather_hist_collection,
                                              weather_fcst_db,
                                              weather_fcst_collection,
                                              granularity)
    common.utils.debug_msg(debug, "wetbulb: %s" % wetbulb_ts)
    print(type(wetbulb_ts))

    # get occupancy data
    occ_ts = ts_proc.utils.get_occupancy_ts(host, port, db_name, username,
                                            password, source,
                                            collection_name, building_id)
    # interpolation converts occupancy data to float; convert back to int64
    # occ_ts = ts_proc.munge.interp_tseries(occ_ts, granularity).astype(
    #     numpy.int64)
    # occ_ts = ts_proc.munge.munge(occ_ts, 100, 2, '1min', granularity).astype(
    #     numpy.int64)
    common.utils.debug_msg(debug, "occupancy: %s" % occ_ts)

    # query steam data
    steam_ts = ts_proc.utils.get_parsed_ts(host, port, db_name, username,
                                           password, source, collection_name,
                                           building_id, 'TotalInstant',
                                           'SIF_Steam_Demand')
    common.utils.debug_msg(debug, "steam: %s" % steam_ts)

    # find baseline
    bench_info = _find_benchmark(base_dt, occ_ts, wetbulb_ts,
                                 steam_ts, granularity, debug)
    bench_dt, bench_auc, bench_incr_auc, bench_usage = bench_info
    common.utils.debug_msg(debug, "bench dt: %s, bench usage: %s, auc: %s" % (
        bench_dt, bench_usage, bench_auc))

    sys.exit(0)

    # TODO: delete display code
    # plot
    # get actual, if available
    # actual_ts = common.utils.get_dt_tseries(base_dt, steam_ts)
    # actual_ts_nodate = common.utils.drop_series_ix_date(actual_ts)
    # print("actual: %s" % actual_ts)
    # disp_df = bench_usage.to_frame(name='benchmark')
    # disp_df = disp_df.join(actual_ts_nodate.to_frame(name='actual'),
    #                        how='outer')
    # print("disp df: %s" % disp_df)

    # matplotlib.pyplot.style.use('ggplot')
    # matplotlib.pyplot.figure()
    # chart = disp_df.plot()
    # fig = chart.get_figure()
    # fig.savefig("bmark_%s.png" % base_dt)

    # save results
    if not debug:
        _save_benchmark(bench_dt, base_dt, bench_usage, bench_auc,
                        bench_incr_auc, host, port, db_name_out, username,
                        password, source, collection_name_out, building_id,
                        'Electric_Demand', 'benchmark')
