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
    utils.process_building(building, bldg_params, cfg['weather'],
                            cfg['sarima'], cfg['sampling'])


