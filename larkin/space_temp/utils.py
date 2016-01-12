# coding=utf-8

__author__ = 'ashishgagneja'

"""
driver for generating start-time using a arima model built using space
temperature data
"""
import dateutil.relativedelta as relativedelta
import pymongo

import larkin.arima.model
from larkin.ts_proc.utils import get_space_temp_ts


def process_building(building_id, host, port, username, password, db_name,
                     collection_name, floor_quadrants, h5file_name,
                     history_name, forecast_name, order, granularity):
    """ Generate startup time using SARIMA model for each floor-quadrant
        combination

    :param building_id: string
        building_id identifier
    :param host: string
        database server name or IP-address
    :param port: int
        database port number
    :param username: string
        database username
    :param password: string
        database password
    :param db_name: string
        name of the database on server
    :param collection_name: string
        name of collection in the database
    :param floor_quadrants: list
        list of floor-quadrants
    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file
    :param order: string
        order params tuple as string for SARIMA model
    :param granularity: int
        sampling frequency of input data and forecast data
    :return:
    """

    # connect to database
    conn = pymongo.MongoClient(host, port, username, password)
    db = conn[db_name]

    predictions = []
    for floor_quadrant in floor_quadrants:
        floor, quad = floor_quadrant
        print('processing %s:%s' % (floor, quad))

        # query data
        ts = get_space_temp_ts(db, collection_name, building_id, floor, quad,
                               granularity)

        pred_dt = ts.index[-1] - 2 * relativedelta.relativedelta(days=1)

        # invoke model
        predictions.append(
                larkin.arima.model.start_time(ts, h5file_name, history_name,
                                              forecast_name, order,
                                              granularity, str(pred_dt)))

    conn.close()
    return predictions
