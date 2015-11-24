
__author__ = 'ashishgagneja'

import pandas as pd
import electric.utils
import weather.helpers
import datetime
import occupancy.utils
import itertools
import weather.wet_bulb
import common.utils
import numpy
import sys
import matplotlib.pyplot




def _filter_missing_weather_data(weather_df):
    """
    Filter/remove rows with missing data like -9999's

    :param weather_df: pandas DataFrame
    :return: pandas DataFrame
    """

    bad_data = weather_df.where(weather_df < -998).any(axis=1)
    return weather_df.drop(bad_data[bad_data == True].index)



def _get_weather(h5file_name, history_name, forecast_name, gran):
    """ Load all available weather data, clean it and drop unneeded columns

    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file
    :param granularity: int
        sampling frequency of input data and forecast data

    :return: pandas DataFrame
    """

    with pd.HDFStore(h5file_name) as store:

        munged_history = weather.helpers.history_munge(store[history_name],
                                                       "%dmin" % gran)

        munged_forecast = weather.helpers.forecast_munge(store[forecast_name],
                                                         "%dmin" % gran)
                                                         # cov, "%dmin" % gran)


    # drop unnecessary columns
    # TODO: this should be done before munging for efficiency but couldn't make
    # it work
    munged_history = munged_history[['temp', 'dewpt', 'pressure']]
    munged_forecast = munged_forecast[['temp', 'dewpoint', 'mslp']]

    # rename forecast columns to match the corresponding historical columns
    munged_forecast = munged_forecast.rename(columns={'dewpoint': 'dewpt',
                                                      'mslp': 'pressure'})

    all_weather = pd.concat([munged_history, munged_forecast])
    return _filter_missing_weather_data(all_weather)



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

    thresh = 0.85 * 24 * 60 / gran
    return set([key for key, cnt in itertools.filterfalse(
        lambda x: x[1] < thresh, counts)])



def _get_wetbulb_ts(weather_df):
    """
    Compute wet bulb temperature time series from weather data
    :param weather_df: pandas DataFrame
    :return: pandas
    """
    return weather_df.apply(weather.wet_bulb.compute_bulb_helper, axis=1)



def find_lowest_electric_usage(date_scores, electric_ts, n):
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

    :return: tuple with benchmark date and pandas Series object with usage data
        from benchmark date
    """

    dates, sim_scores = zip(*date_scores)

    min_usage = [dates[0], sys.maxsize, None]
    for i, dt in enumerate(dates):

        if i >= n:
            break

        score = sim_scores[i]
        if score:

            # compute day electric usage by integrating the curve
            # Assumption: Linear interpolation is a reasonable way to fill gaps
            day_elec_ts = common.utils.drop_series_ix_date(
                common.utils.get_dt_tseries(dt, electric_ts))
            auc = numpy.trapz(day_elec_ts.data, x=list(map(lambda x:
                                                           x.hour * 3600
                                                         + x.minute * 60
                                                         + x.second,
                                                           day_elec_ts.index)))
            print("%s, %s" % (dt, auc))

            if 0 < auc < min_usage[1]:
                min_usage = [dt, auc, day_elec_ts]

    return min_usage[0], min_usage[2]



def _find_benchmark(base_dt, occ_ts, wetbulb_ts, electric_ts, gran):
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
    :param granularity: int
        expected frequency of observations and forecast in minutes

    :return: tuple containing benchmark date and a pandas Series object with
        electric usage data from that date
    """

    # get data availability
    elec_avlblty = _get_data_availability_dates(electric_ts, gran)
    occ_avlblty = _get_data_availability_dates(occ_ts, gran)
    data_avlblty = occ_avlblty.intersection(elec_avlblty)

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
    print("sim days: %s" % str(sim_wetbulb_days))

    # compute occupancy similarity score for the k most similar weather days
    occ_scores = occupancy.utils.score_occ_similarity(base_dt, sim_wetbulb_days,
                                                      occ_ts)
    print(occ_scores)
    # find the date with the lowest electric usage
    return find_lowest_electric_usage(occ_scores, electric_ts, 5)



def process_building(building_id, db_server, db_name, collection_name,
                     meter_count, h5file_name, history_name, forecast_name,
                     granularity, base_dt):

    """ Find baseline electric usage for building_id

    :param building_id: string
        building_id identifier
    :param db_server: string
        database server name or IP-address
    :param db_name: string
        name of the database on server
    :param collection_name: string
        name of collection in the database
    :param meter_count: int
        number of electric meters
    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file
    :param granularity: int
        expected frequency of observations and forecast in minutes
    :param base_dt: datetime.date
        date for which benchmark electric usage is to be found
    :return:
    """

    # get occupancy data
    occ_ts = occupancy.utils.get_occupancy_ts(db_server, db_name,
                                              collection_name, building_id)
    print("occupancy: %s" % occ_ts)

    # query electric data
    elec_ts = electric.utils.get_electric_ts(db_server, db_name,
                                             collection_name, building_id,
                                             meter_count, granularity)
    print("electric: %s" % elec_ts)

    # get weather
    weather_df = _get_weather(h5file_name, history_name, forecast_name,
                              granularity)
    print("weather: %s" % weather_df)
    wetbulb_ts = _get_wetbulb_ts(weather_df)
    print("wetbulb: %s" % wetbulb_ts)

    # find baseline
    bench_dt, bench_usage = _find_benchmark(base_dt, occ_ts, wetbulb_ts,
                                            elec_ts, granularity)
    print("bench dt: %s, bench usage: %s" % (bench_dt, bench_usage))

    # TODO: delete display code
    # plot
    # get actual, if available
    actual_ts = common.utils.get_dt_tseries(base_dt, elec_ts)
    actual_ts_nodate = common.utils.drop_series_ix_date(actual_ts)
    disp_df = bench_usage.to_frame(name='benchmark')
    disp_df = disp_df.join(actual_ts_nodate.to_frame(name='actual'),
                           how='outer')
    print("disp df: %s" % disp_df)

    matplotlib.pyplot.style.use('ggplot')
    matplotlib.pyplot.figure()
    chart = disp_df.plot()
    fig = chart.get_figure()
    fig.savefig('bmark.png')

    # TODO: save results
