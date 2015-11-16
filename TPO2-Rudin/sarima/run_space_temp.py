__author__ = 'ashishgagneja'

"""
driver for generating start-time using a SARIMA model for space
temperature data
"""

import config
import space_temp.utils as utils


cfg = config.ashish

buildings = cfg['default']['buildings']

# iterate over all buildings
for building in buildings:

    bldg_params = cfg[building]
    weather_params = cfg['weather']
    sarima_params = cfg['sarima']
    sampling_params = cfg['sampling']

    utils.process_building(building, bldg_params['db_server_input'],
                           bldg_params['db_name_input'],
                           bldg_params['collection_name_input'],
                           bldg_params['floor_quadrants'],
                           weather_params['h5file'],
                           weather_params['history'],
                           weather_params['forecast'],
                           sarima_params['order'],
                           sarima_params['enforce_stationarity'],
                           sampling_params['granularity'])


