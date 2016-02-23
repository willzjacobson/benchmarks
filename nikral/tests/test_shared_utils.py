# coding=utf-8

__author__ = 'ashishgagneja'

import unittest
import datetime

import numpy as np
import pandas as pd
import pytz

import nikral.shared.utils as utils


class TestSharedUtils(unittest.TestCase):


    def _gen_ts(self, begin, end, gran):
        test_idx = pd.DatetimeIndex(start=begin, end=end, freq="%dmin" % gran)
        return pd.Series(data=np.random.rand(test_idx.size), index=test_idx)


    def test_series_ix_date(self):
        test_idx = pd.DatetimeIndex(start=datetime.datetime(2015, 1, 1, 1),
                                    end  =datetime.datetime(2015, 1, 1, 22, 45),
                                    freq ="15min")

        data = np.random.rand(test_idx.size)
        test_ts = pd.Series(data=data, index=test_idx)
        ret_ts = utils.drop_series_ix_date(test_ts)
        for key in ret_ts.index:
            self.assertTrue(isinstance(key, datetime.time))


    def test_get_dt_tseries(self):
        tzone = pytz.timezone('US/Eastern')
        test_ts = self._gen_ts(datetime.datetime(2015, 5, 11, 8),
                               datetime.datetime(2015, 5, 31, 19),
                               15).tz_localize(pytz.utc).tz_convert(tzone)

        test_dt = datetime.date(2015, 5, 12)
        ret_ts = utils.get_dt_tseries(test_dt, test_ts, tzone)
        ret_ts_short = utils.get_dt_tseries(test_dt, test_ts, tzone, True)

        self.assertTrue(ret_ts_short.size < ret_ts.size)

        for tmp_ts in [ret_ts, ret_ts_short]:
            for idx in tmp_ts.index:
                self.assertTrue(idx.date() == test_dt)


    def test_dow_type(self):

        tmp_dt = datetime.date(2015, 1, 1)
        tm_delta = datetime.timedelta(days=1)

        dow_typ_dict = {}
        while tmp_dt < datetime.date(2015, 4, 1):
            tmp_dow = tmp_dt.isoweekday()

            if tmp_dow not in dow_typ_dict:
                dow_typ_dict[tmp_dow] = utils.dow_type(tmp_dt)
            else:
                self.assertTrue(dow_typ_dict[tmp_dow] == utils.dow_type(tmp_dt))
            tmp_dt += tm_delta
