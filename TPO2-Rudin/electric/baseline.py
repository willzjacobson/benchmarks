__author__ = 'ashishgagneja'

import db.connect as connect
import pandas as pd
import dateutil.parser
import electric.utils


def _get_weather(h5file_name, history_name, forecast_name):
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

    weather_history = store[history_name]
    weather_forecast = store[forecast_name]
    store.close()

    print("forecast: %s" % weather_forecast)
    print("history: %s" % weather_history)
    return [weather_history, weather_forecast]



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

    # get weather data
    _get_weather(h5file_name, history_name, forecast_name)

    # query electric data
    electric.utils.get_electric_ts(db, collection_name, building_id,
                                   meter_count, granularity)

    # find baseline

    # TODO: save results
    conn.close()
