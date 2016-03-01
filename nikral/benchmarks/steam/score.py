# coding=utf-8
__author__ = 'ashishgagneja'

import sys

import nikral.benchmarks.utils as butils


# cfg = dict(user_config, **model_config)


def main():
    """
    driver for scoring steam benchmark results
    """

    # determine date to compute score for
    score_dt = butils.get_score_dt(sys.argv)
    print("scoring steam benchmark for %s" % score_dt)


    # get benchmark result
    # get actual
    # score
    # save score



if __name__ == '__main__':
    main()