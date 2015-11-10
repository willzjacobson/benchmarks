__author__ = 'ashishgagneja'


"""
driver for obtaining baseline electric demand based on occupancy and weather
co-variates
"""

import config
import baseline


cfg = config.ashish

buildings = cfg['default']['buildings']
# iterate over all buildings
for building in buildings:

    bldg_params = cfg[building]
    baseline.process_building(building, bldg_params, cfg['weather'],
                           cfg['sampling'])
