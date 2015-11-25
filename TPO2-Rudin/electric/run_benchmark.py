__author__ = 'ashishgagneja'

"""
driver for obtaining baseline electric demand based on occupancy and weather
co-variates
"""

import config
import electric.benchmark as bmark
import sys
import datetime

cfg = config.ashish

buildings = cfg['default']['buildings']


# determine benchmark date
bench_dt = datetime.date.today()


arg_count = len(sys.argv)
if arg_count not in [1, 4]:
    raise Exception("Usage: python %s [YYYY MM DD]"
                    % sys.argv[0])

elif arg_count == 4:
    int_args = list(map(int, sys.argv[1:]))
    bench_dt = datetime.date(int_args[0], int_args[1], int_args[2])

print("looking up benchmark for %s" % bench_dt)

# iterate over all buildings
for building_id in buildings:

    bldg_params = cfg[building_id]
    bmark.process_building(building_id,
                           bldg_params['db_server_input'],
                           bldg_params['db_name_input'],
                           bldg_params['collection_name_input'],
                           # use the input db for now for output
                           bldg_params['db_name_input'],
                           bldg_params['collection_name_out'],
                           bldg_params['electric_meter_count'],
                           cfg['weather']['h5file'],
                           cfg['weather']['history_orig'],
                           cfg['weather']['forecast_orig'],
                           cfg['sampling']['granularity'],
                           bench_dt)
