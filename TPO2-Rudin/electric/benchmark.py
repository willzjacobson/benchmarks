__author__ = 'ashishgagneja'

import db.connect as connect
import pandas as pd
import electric.utils
import weather.helpers
import datetime
import occupancy.utils
import itertools
import weather.wet_bulb


def _filter_missing_weather_data(weather_df):
    """
    Filter rows with missing data like -9999's

    :param weather_df: pandas DataFrame

    :return: pandas DataFrame
    """

    bad_data = weather_df.where(weather_df < -998).any(axis=1)
    print('bad_data: %s' % bad_data[bad_data == True].shape)
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

        # cov = ['temp', 'dewpt', 'pressure']
        history = store[history_name]
        # munged_history = weather.helpers.history_munge(store[history_name], cov,
        munged_history = weather.helpers.history_munge(store[history_name],
                                                       "%dmin" % gran)
        # cov = ['temp', 'dewpoint', 'mslp']

        fcst = store[forecast_name]
        # fcst = fcst[['temp', 'dewpt', 'pressure']]
        munged_forecast = weather.helpers.forecast_munge(store[forecast_name],
                                                         "%dmin" % gran)
                                                         # cov, "%dmin" % gran)


    # drop unnecessary columns
    # TODO: this should be done before munging for efficiency but couldn't make
    # it to work
    munged_history = munged_history[['temp', 'dewpt', 'pressure']]
    munged_forecast = munged_forecast[['temp', 'dewpoint', 'mslp']]

    # rename forecast columns to match the corresponding historical columns
    munged_forecast = munged_forecast.rename(columns={'dewpoint': 'dewpt',
                                                      'mslp': 'pressure'})

    # print("forecast: %s" % munged_forecast)
    # print("history: %s" % munged_history)
    all_weather = pd.concat([munged_history, munged_forecast])

    # print(all_weather)
    # _filter_missing_weather_data(all_weather)
    return _filter_missing_weather_data(all_weather)
    # return _filter_missing_weather_data(all_weather)



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



def _get_wet_bulb_ts(weather_df):
    return weather_df.apply(weather.wet_bulb.compute_bulb_helper, axis=1)



def _get_dt_wetbulb(wetbulb_ts):
    pass



def _find_benchmark(bench_dt, occ_ts, weather_ts, electric_ts, gran):

    # get data availability
    elec_avlblty = _get_data_availability_dates(electric_ts, gran)
    occ_avlblty = _get_data_availability_dates(occ_ts, gran)
    data_avlblty = occ_avlblty.intersection(elec_avlblty)

    # get weather for bench_dt


    # find closest weather days for which electric and occupancy data is
    # available





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
    print(occ_ts)

    # get weather data
    weather_df = _get_weather(h5file_name, history_name, forecast_name,
                              granularity)
    print("weather: %s" % weather_df)
    wet_bulb_ts = _get_wet_bulb_ts(weather_df)
    print("wetbulb: %s" % wet_bulb_ts)

    # query electric data
    elec_ts = electric.utils.get_electric_ts(db, collection_name, building_id,
                                   meter_count, granularity)

    # find baseline
    _find_benchmark(bench_dt, occ_ts, weather_df, elec_ts, granularity)

    # TODO: save results
    conn.close()
