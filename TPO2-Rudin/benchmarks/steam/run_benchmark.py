# coding=utf-8
__author__ = 'ashishgagneja'

"""
driver for obtaining baseline steam demand based on occupancy and weather
co-variates
"""

import datetime
import sys

import config
import benchmarks.steam.benchmark as bmark

cfg = config.david

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

bldg_results = cfg['building_dbs']['results']

# iterate over all buildings
for building_id in buildings:

    bldg_params = cfg['default'][building_id]
    bmark.process_building(
        building_id,
        # host=bldg_params['host'],
        # port=bldg_params['port'],
        # db_name=bldg_params['database'],
        # username=bldg_params['username'],
        # password=bldg_params['password'],
        # source=bldg_params['source_db'],
        # collection_name=bldg_params['collection_name_input'],
        # use the input db for now for output
        # database_out=bldg_params['database'],
        database_out=bldg_results[''],
        collection_name_out=bldg_params['collection_name_out'],
        # h5file_name=cfg['building_dbs']['h5file'],
        # history_name=cfg['building_dbs']['history_orig'],
        # forecast_name=cfg['building_dbs']['forecast_orig'],
        granularity=cfg['sampling']['granularity'],
        base_dt=bench_dt,
        debug=cfg['default']['debug']
        **cfg['building_dbs']['mongo_cred']
        **cfg['building_id']['building_ts_loc'])
