# coding=utf-8
__author__ = 'ashishgagneja'

"""
driver for obtaining baseline electric demand based on occupancy and weather
co-variates
"""

import datetime
import sys

import __init__
from larkin import benchmarks as bmark

cfg = __init__.config

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

# fill keyword argument dict
kw_args = dict(dict(cfg['building_dbs']['mongo_cred'],
                    **cfg['building_dbs']['building_ts_loc']),
               **cfg['building_dbs']['results'])

weather_hist = cfg['building_dbs']['weather_history_loc']
weather_fcst = cfg['building_dbs']['weather_forecast_loc']

kw_args['weather_hist_db']         = weather_hist['db_name']
kw_args['weather_hist_collection'] = weather_hist['collection_name']
kw_args['weather_fcst_db']         = weather_fcst['db_name']
kw_args['weather_fcst_collection'] = weather_fcst['collection_name']

kw_args['granularity'] = cfg['sampling']['granularity']
kw_args['base_dt']     = bench_dt
kw_args['debug']       = cfg['default']['debug']


# iterate over all buildings
for building_id in buildings:

    bldg_params = cfg['default'][building_id]
    bmark.process_building(building_id,
                           # bldg_params['host'],
                           # bldg_params['port'],
                           # bldg_params['database'],
                           # bldg_params['username'],
                           # bldg_params['password'],
                           # bldg_params['source_db'],
                           # bldg_params['collection_name_input'],
                           # use the input db for now for output
                           # bldg_params['database'],
                           # bldg_params['collection_name_out'],
                           meter_count=bldg_params['electric_meter_count'],
                           # cfg['building_dbs']['h5file'],
                           # cfg['building_dbs']['history_orig'],
                           # cfg['building_dbs']['forecast_orig'],
                           # cfg['sampling']['granularity'],
                           # bench_dt,
                           # cfg['default']['debug'])
                           **kw_args)
