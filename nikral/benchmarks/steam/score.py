# coding=utf-8
__author__ = 'ashishgagneja'

import sys
import re

import nikral.benchmarks.utils as butils
from nikral.user_config import user_config
from nikral.model_config import model_config
import nikral.ts_proc.utils as ts_utils

cfg = dict(user_config, **model_config)

def main():
    """
    driver for scoring steam benchmark results
    """

    # determine date to compute score for
    score_dt = butils.get_score_dt(sys.argv)
    print("scoring steam benchmark for %s" % score_dt)

    for building in cfg['default']['buildings']:
        # bldg_params = cfg['default'][building]
        # print(cfg['building_dbs']['mongo_cred'])
        bmark_cfg = cfg['building_dbs']['results_steam_benchmark']
        gran = cfg['sampling']['granularity']
        gran_int = int(re.findall('\d+', gran)[0])

        # bldg_ts_cfg = cfg['building_dbs']['building_ts_loc']

        # get benchmark result
        bench_ts = butils.get_bench_ts(bench_dt=score_dt,
                                       collection_name=bmark_cfg[
                                           'collection_name_out'],
                                       database=bmark_cfg['db_name_out'],
                                       building=building,
                                       bmark_type='building',
                                       system='Steam_Usage',
                                       **cfg['building_dbs'][
                                           'mongo_cred'])

        bench_ts = butils.readings_to_ts(bench_ts)
        print(bench_ts)

        kw_args = dict(cfg['building_dbs']['building_ts_loc'],
                       **cfg['building_dbs']['mongo_cred'])
        # get actual
        # ts_utils.get_date_ts(building=building,
                             # database=bldg_ts_cfg['db_name'],
                             # collection_name=bldg_ts_cfg['collection_name'],
                             # dt=score_dt,
                             # devices='TotalInstant',
                             # **kw_args)
        actual_ts = ts_utils.get_parsed_ts_new_schema(building=building,
                                                      devices='TotalInstant',
                                                      ts_date=score_dt,
                                                      **kw_args)
        actual_ts = butils.align_idx(actual_ts, gran_int)
        print(actual_ts)

        # score
        rmse = butils.get_rmse_score(actual_ts, bench_ts, gran_int)
        print(rmse)

        # save score




if __name__ == '__main__':
    main()