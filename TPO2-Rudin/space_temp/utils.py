__author__ = 'ashishgagneja'

"""
driver for generating start-time using a sarima model built using space
temperature data
"""

import utils.connect as connect
import pandas as pd
import dateutil as du
import sarima.model as model
import dateutil.relativedelta as relativedelta

def _get_space_temp_ts(db, collection_name, bldg, floor, quad, granularity):
    """ retrieve all available space temperature data for floor-quad of
        building bldg

    :param db: pymongo database object
        connected database object
    :param bldg: string
        database building identifier
    :param floor: string
        floor identifier
    :param quad: string
        quadrant identifier
    :return: pandas Series
    """

    ts_list, value_list = [], []
    collection = db[collection_name]
    for data in collection.find({"_id.building": bldg,
                                 "_id.device": "Space_Temp",
                                 "_id.floor": floor,
                                 "_id.quad": quad}):
        readings = data['readings']
        for reading in readings:
            ts_list.append(du.parser.parse(reading['time'], ignoretz=True))
            value_list.append(float(reading['value']))

    gran = "%dmin" % granularity
    return pd.Series(data=value_list, index=pd.DatetimeIndex(ts_list)
                   ).sort_index().resample(gran)



def _process_building(building_id, bldg_params, weather_params, sarima_params,
                      sampling_params):
    """ Generate startup time using SARIMA model for each floor-quadrant
        combination

    :param building_id: string
        building identifier
    :param bldg_params: dict
        configuration settings of the building
    :param weather_params: dict
        weather configuration
    :param sarima_params: dict
        configuration for SARIMA model
    :param sampling_params: dict
        sampling-related configuration
    :return:
    """

    # connect to database
    conn = connect.connect(bldg_params['db_server_input'],
                           database=bldg_params["db_name_input"])
    db = conn[bldg_params["db_name_input"]]

    for floor_quadrant in bldg_params['floor_quadrants']:
        floor, quad = floor_quadrant
        print('processing %s:%s' % (floor, quad))

        # query data
        ts = _get_space_temp_ts(db, bldg_params["collection_name_input"],
                                building_id, floor, quad,
                                sampling_params['granularity'])

        pred_dt = ts.index[-1] - 2*relativedelta.relativedelta(days=1)

        # invoke model
        prediction = model.start_time(ts, weather_params, sarima_params,
                                      sampling_params['granularity'],
                                      str(pred_dt))


    # TODO: save results
    conn.close()