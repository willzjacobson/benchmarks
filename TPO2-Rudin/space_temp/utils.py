__author__ = 'ashishgagneja'

"""
driver for generating start-time using a sarima model built using space
temperature data
"""
import dateutil.parser
import dateutil.relativedelta as relativedelta
import pandas as pd
import pymongo

import sarima.model


def get_space_temp_ts(db, collection_name, bldg, floor, quad, granularity):
    """ retrieve all available space temperature data for floor-quad of
        building_id bldg

    :param db: pymongo database object
        connected database object
    :param bldg: string
        database building_id identifier
    :param floor: string
        floor identifier
    :param quad: string
        quadrant identifier
    :param granularity: int
    sampling frequency of input data and forecast data

    :return: pandas Series
    """

    ts_list, value_list = [], []
    collection = db[collection_name]
    for data in collection.find({"_id.building": bldg,
                                 "_id.device": "Space_Temp",
                                 "_id.floor": str(floor),
                                 "_id.quad": quad}):
        readings = data['readings']
        for reading in readings:
            ts_list.append(
                    dateutil.parser.parse(reading['time'], ignoretz=True))
            value_list.append(float(reading['value']))

    gran = "%dmin" % granularity
    return pd.Series(data=value_list, index=pd.DatetimeIndex(ts_list)
                     ).sort_index().resample(gran)


def process_building(building_id, host, port, username, password,
                     db_name, collection_name,
                     floor_quadrants, h5file_name, history_name, forecast_name,
                     order, enforce_stationarity, granularity):
    """ Generate startup time using SARIMA model for each floor-quadrant
        combination

    :param building_id: string
        building_id identifier
    :param host: string
        database server name or IP-address
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
    :param enforce_stationarity: boolean
        whether to enforce stationarity in the SARIMA model
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
                sarima.model.start_time(ts, h5file_name, history_name,
                                        forecast_name, order,
                                        enforce_stationarity,
                                        granularity, str(pred_dt)))

    # TODO: save results
    conn.close()
    return predictions
