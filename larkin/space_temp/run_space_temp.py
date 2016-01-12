# coding=utf-8

__author__ = 'ashishgagneja'

"""
driver for generating start-time using a ARIMA model for space
temperature data
"""

import dateutil.relativedelta as relativedelta
import pymongo

import __init__
import larkin.arima.model
import larkin.ts_proc.munge

cfg = __init__.config

buildings = cfg['default']['buildings']

# iterate over all buildings
for building in buildings:

    bldg_params = cfg[building]
    weather_params = cfg['building_dbs']
    arima_params = cfg['arima']
    granularity = cfg['sampling']['granularity']

    # connect to database
    conn = pymongo.MongoClient(bldg_params['host'], bldg_params['port'])
    conn[bldg_params['database']].authenticate(bldg_params['username'],
                                               bldg_params['password'],
                                               source=bldg_params['source_db'])
    db = conn[bldg_params['database']]

    predictions = []
    for floor_quadrant in bldg_params['floor_quadrants']:
        floor, quad = floor_quadrant

        # get space temp time series
        ts = larkin.ts_proc.utils.get_space_temp_ts(db,
                                                    bldg_params['collection_name_input'],
                                                    building, floor, quad, granularity)

        pred_dt = ts.index[-1] - 2 * relativedelta.relativedelta(days=1)
        print(pred_dt)

        # invoke model
        forecast, std_err, conf_int = larkin.arima.model.start_time(
            larkin.ts_proc.munge.interp_tseries(ts, granularity),
            weather_params['h5file'],
                weather_params['weather_history_loc'],
                weather_params['weather_forecast_loc'],
            arima_params['order'],
            granularity,
            str(pred_dt))

        print("forecast: %s" % forecast)
        print("std err: %s" % std_err)
        print("confidence interval: %s" % conf_int)

    conn.close()


