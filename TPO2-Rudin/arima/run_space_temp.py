__author__ = 'ashishgagneja'

"""
driver for generating start-time using a ARIMA model for space
temperature data
"""

import config
import space_temp.utils
import dateutil.relativedelta as relativedelta
import arima.model
import common.utils


cfg = config.ashish

buildings = cfg['default']['buildings']

# iterate over all buildings
for building in buildings:

    bldg_params = cfg[building]
    weather_params = cfg['weather']
    arima_params = cfg['arima']
    granularity = cfg['sampling']['granularity']

    predictions = []
    for floor_quadrant in bldg_params['floor_quadrants']:
        floor, quad = floor_quadrant

        ts = space_temp.utils.get_space_temp_ts(bldg_params['host'],
                    bldg_params['port'], bldg_params['database'],
                    bldg_params['username'], bldg_params['password'],
                    bldg_params['source_db'],
                    bldg_params['collection_name_input'],
                    building, floor, quad, granularity)

        pred_dt = ts.index[-1] - 2 * relativedelta.relativedelta(days=1)
        print(pred_dt)

        # invoke model
        predictions.append(arima.model.start_time(
            common.utils.interp_tseries(ts, granularity),
            weather_params['h5file'],
            weather_params['history'],
            weather_params['forecast'],
            arima_params['order'],
            granularity,
            str(pred_dt)))

    print(predictions)


