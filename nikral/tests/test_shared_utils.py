# coding=utf-8

__author__ = 'ashishgagneja'

import unittest
import datetime

import numpy as np
import pandas as pd

import nikral.shared.utils as utils


class TestBmarkUtils(unittest.TestCase):

    def test_series_ix_date(self):
        test_idx = pd.DatetimeIndex(start=datetime.datetime(2015, 1, 1, 1),
                                    end  =datetime.datetime(2015, 1, 1, 22, 45),
                                    freq ="15min")

        data = np.random.rand(test_idx.size)
        test_ts = pd.Series(data=data, index=test_idx)
        ret_ts = utils.drop_series_ix_date(test_ts)
        for key in ret_ts.index:
            self.assertTrue(isinstance(key, datetime.time))
