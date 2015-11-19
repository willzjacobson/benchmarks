__author__ = 'ashishgagneja'

"""
driver for obtaining baseline electric demand based on occupancy and weather
co-variates
"""

import config
import electric.benchmark as bmark

cfg = config.ashish

buildings = cfg['default']['buildings']

# determine benchmark date


# iterate over all buildings
for building_id in buildings:

    bldg_params = cfg[building_id]
    bmark.process_building(building_id,
                           bldg_params['db_server_input'],
                           bldg_params['db_name_input'],
                           bldg_params['collection_name_input'],
                           bldg_params['electric_meter_count'],
                           cfg['weather']['h5file'],
                           cfg['weather']['history_orig'],
                           cfg['weather']['forecast_orig'],
                           cfg['sampling']['granularity'],
                           None)
