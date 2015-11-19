__author__ = 'ashishgagneja'

import db.connect as connect
import pandas as pd
import electric.utils
import weather.helpers
import datetime
import occupancy.utils
import itertools
import weather.wet_bulb
import common.utils
import dateutil.relativedelta


def _filter_missing_weather_data(weather_df):
    """
    Filter rows with missing data like -9999's

    :param weather_df: pandas DataFrame

    :return: pandas DataFrame
    """

    bad_data = weather_df.where(weather_df < -998).any(axis=1)
    print('bad_data: %s' % bad_data[bad_data == True])
    return weather_df.drop(bad_data[bad_data == True].index)


def _get_weather(h5file_name, history_name, forecast_name, gran):
    """

    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file
    :return:
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
    Find dates for which data is available. Dates for which < threshold % data
    is available are dropped.

    Assumption: Series has no NA's
    Assumption: Threshold is 85

    :param obs_ts: pandas Series
    :param gran: int
        sampling frequency of input data and forecast data
    :return: set of dates for which
    """

    ts_list = list(map(datetime.datetime.date, obs_ts.index))
    counts = [[key, len(list(grp))] for key, grp in itertools.groupby(ts_list)]

    thresh = 0.85 * 24 * 60 / gran
    return set([key for key, cnt in itertools.filterfalse(
        lambda x: x[1] < thresh, counts)])



def _get_wetbulb_ts(weather_df):
    return weather_df.apply(weather.wet_bulb.compute_bulb_helper, axis=1)



def _get_dt_wetbulb(dt, wetbulb_ts):

    # zipped = zip(list[wetbulb_ts.index.map(lambda x: x.date())],
    #              wetbulb_ts.index)
    # zipped = zip(list[wetbulb_ts.index.date(lambda x: x.date())],
    #              wetbulb_ts.index)
    bod_tm = datetime.time(0, 0, 0, 0)
    start_idx = datetime.datetime.combine(dt, bod_tm)
    end_idx = datetime.datetime.combine(
        dt + dateutil.relativedelta.relativedelta(days=1), bod_tm)
    return wetbulb_ts[str(start_idx) : str(end_idx)]

    # dt_indices = list[map(lambda x, y: y if x == dt else pass, zipped)]



def _find_benchmark(bench_dt, occ_ts, wetbulb_ts, electric_ts, gran):

    # get data availability
    elec_avlblty = _get_data_availability_dates(electric_ts, gran)
    occ_avlblty = _get_data_availability_dates(occ_ts, gran)
    data_avlblty = occ_avlblty.intersection(elec_avlblty)

    # get weather for bench_dt
    bench_dt_wetbulb = _get_dt_wetbulb(bench_dt, wetbulb_ts)

    # find k closest weather days for which electric and occupancy data is
    # available
    sim_wetbulb_days = common.utils.find_similar_profile_days(bench_dt_wetbulb,
                                                              wetbulb_ts,
                                                              20,
                                                              data_avlblty)
    print("sim days: %s" % str(sim_wetbulb_days))







def process_building(building_id, db_server, db_name, collection_name,
                     meter_count, h5file_name, history_name, forecast_name,
                     granularity, bench_dt):

    """ Find baseline electric usage for building_id

    :param building_id: string
        building_id identifier
    :param db_server: string
        database server name or IP-address
    :param db_name: string
        name of the database on server
    :param collection_name: string
        name of collection in the database
    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file
    :param granularity: int
        expected frequency of observations and forecast in minutes
    :return:
    """

    # connect to database
    conn = connect.connect(db_server, database=db_name)
    db = conn[db_name]


    # TODO: query occupancy data
    occ_ts = occupancy.utils.get_occupancy_ts(db, collection_name, building_id)
    print("occupancy: %s" % occ_ts)

    # get weather data
    weather_df = _get_weather(h5file_name, history_name, forecast_name,
                              granularity)
    print("weather: %s" % weather_df)
    wetbulb_ts = _get_wetbulb_ts(weather_df)
    print("wetbulb: %s" % wetbulb_ts)

    # query electric data
    elec_ts = electric.utils.get_electric_ts(db, collection_name, building_id,
                                   meter_count, granularity)

    # find baseline
    _find_benchmark(bench_dt, occ_ts, wetbulb_ts, elec_ts, granularity)

    # TODO: save results
    conn.close()
