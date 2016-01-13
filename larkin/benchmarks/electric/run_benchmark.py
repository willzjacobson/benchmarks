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
                           timezone=bldg_params['timezone'],
                           meter_count=bldg_params['electric_meter_count'],
                           **kw_args)

