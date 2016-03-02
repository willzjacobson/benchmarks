# coding=utf-8
__author__ = 'ashishgagneja'

import sys

import nikral.benchmarks.utils as butils
from nikral.user_config import user_config
import nikral.ts_proc.utils as ts_utils


def main():
    """
    driver for scoring steam benchmark results
    """

    # determine date to compute score for
    score_dt = butils.get_score_dt(sys.argv)
    print("scoring steam benchmark for %s" % score_dt)

    for building in user_config['default']['buildings']:
        # bldg_params = cfg['default'][building]
        # print(user_config['building_dbs']['mongo_cred'])
        bmark_cfg = user_config['building_dbs']['results_steam_benchmark']
        # bldg_ts_cfg = user_config['building_dbs']['building_ts_loc']

        # get benchmark result
        bench_ts = butils.get_bench_ts(bench_dt=score_dt,
                                       collection_name=bmark_cfg[
                                           'collection_name_out'],
                                       database=bmark_cfg['db_name_out'],
                                       building=building,
                                       bmark_type='building',
                                       system='Steam_Usage',
                                       **user_config['building_dbs'][
                                           'mongo_cred'])

        print(bench_ts)
        print(butils.readings_to_ts(bench_ts))

        kw_args = dict(user_config['building_dbs']['building_ts_loc'],
                       **user_config['building_dbs']['mongo_cred'])
        # get actual
        # ts_utils.get_date_ts(building=building,
                             # database=bldg_ts_cfg['db_name'],
                             # collection_name=bldg_ts_cfg['collection_name'],
                             # dt=score_dt,
                             # devices='TotalInstant',
                             # **kw_args)
        actual_ts = ts_utils.get_parsed_ts_new_schema1(building=building,
                                                       devices='TotalInstant',
                                                       ts_date=score_dt,
                                                       **kw_args)
        print(actual_ts)

        # score

        # save score




if __name__ == '__main__':
    main()