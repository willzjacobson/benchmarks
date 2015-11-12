__author__ = 'ashishgagneja'

import db.connect as connect
import pandas as pd
import dateutil.parser
import electric.utils


def _get_weather(params):

    h5file = params["h5file"]
    history_original_name = params["history_orig"]
    forecast_name = params["forecast"]
    store = pd.HDFStore(h5file)

    weather_history = store[history_original_name]
    weather_forecast = store[forecast_name]
    store.close()

    print("forecast: %s" % weather_forecast)
    print("history: %s" % weather_history)
    return [weather_history, weather_forecast]



def _get_ts(db, collection_name, bldg, device, granularity):
    """ retrieve all available data of the specified device type

    :param db: pymongo database object
        connected database object
    :param bldg: string
        database building identifier
    :return: pandas Series
    """

    ts_list, value_list = [], []
    collection = db[collection_name]

    for data in collection.find({"_id.building": bldg,
                                 "_id.device": "Space_Temp"}):

        readings = data['readings']
        for reading in readings:
            ts_list.append(
                dateutil.parser.parse(reading['time'], ignoretz=True))
            value_list.append(float(reading['value']))

    gran = "%dmin" % granularity
    return pd.Series(data=value_list, index=pd.DatetimeIndex(ts_list)
                     ).sort_index().resample(gran)




def process_building(building_id, bldg_params, weather_params, sampling_params,
                     baseline_dt):
    """ Find baseline electric usage for building

    :param building_id: string
        building identifier
    :param bldg_params: dict
        configuration settings of the building
    :param weather_params: dict
        weather configuration
    :param sampling_params: dict
        sampling-related configuration
    :return:
    """

    # connect to database
    conn = connect.connect(bldg_params['db_server_input'],
                           database=bldg_params["db_name_input"])
    db = conn[bldg_params["db_name_input"]]


    # TODO: query occupancy data

    # get weather data
    _get_weather(weather_params)


    # TODO: query electric data
    electric.utils.get_electric_ts(db, bldg_params["collection_name_input"],
                                   building_id, 6,
                                   sampling_params['granularity'])

    # find baseline

    # TODO: save results
    conn.close()
