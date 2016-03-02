# coding=utf-8
__author__ = 'ashishgagneja'

import sys

import nikral.benchmarks.utils as butils
from nikral.user_config import user_config


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
        # print(butils.readings_to_df(bench_ts))

        # get actual
        # ts_utils.get_date_ts(score_dt)

        # score

        # save score




if __name__ == '__main__':
    main()