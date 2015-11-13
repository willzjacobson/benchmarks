__author__ = 'ashishgagneja'

import db.connect as connect
import pandas as pd
import electric.utils
import weather.helpers
import occupancy.utils

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

    store = pd.HDFStore(h5file_name)

    cov = ['temp', 'hum', 'pressure']
    munged_history = weather.helpers.history_munge(store[history_name], cov,
                                                   "%dmin" % gran)
    cov = ['temp', 'dewpoint', 'mslp']
    munged_forecast = weather.helpers.forecast_munge(store[forecast_name], cov,
                                                     "%dmin" % gran)
    store.close()

    print("forecast: %s" % munged_forecast)
    print("history: %s" % munged_history)
    return [munged_history, munged_forecast]




def _find_benchmark(occupancy, weather, electric):
    pass




def process_building(building_id, db_server, db_name, collection_name,
                     meter_count, h5file_name, history_name, forecast_name,
                     granularity, baseline_dt):

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
    # occ_ts = occupancy.utils.get_occupancy_ts(db, collection_name, building_id)
    # print(occ_ts)

    # get weather data
    weather_df = _get_weather(h5file_name, history_name, forecast_name,
                              granularity)

    # query electric data
    elec_ts = electric.utils.get_electric_ts(db, collection_name, building_id,
                                   meter_count, granularity)

    # find baseline
    _find_benchmark(occ_ts, weather_df, elec_ts)

    # TODO: save results
    conn.close()
