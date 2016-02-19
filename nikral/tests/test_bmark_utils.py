# coding=utf-8

__author__ = 'ashishgagneja'

import unittest
import datetime

import pytz
import pandas as pd
import numpy as np

import nikral.benchmarks.utils as utils


class TestBmarkUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.holidays = utils.gen_holidays(datetime.date(2012, 1, 1),
                                          datetime.date(
                                            datetime.date.today().year, 12, 31),
                                          '345_Park')


    def test_gen_holidays(self):
        """
        test gen_holidays()
        """

        # count yearly-wise holidays
        yearwise_counts = {}
        for hol in self.holidays:
            if hol.year not in yearwise_counts:
                yearwise_counts[hol.year] = 0
            yearwise_counts[hol.year] += 1

        for year, hol_count in yearwise_counts.iteritems():
            self.assertTrue(hol_count >= 10)


    def test_is_holiday(self):
        for hol in self.holidays:
            self.assertTrue(utils.is_holiday(hol, self.holidays))


    def test_align_idx(self):
        start_idx = [datetime.datetime(2015, 10, 20, 1,  15, 20, 600),
                     datetime.datetime(2015, 10, 20, 1,  30,  6, 220),
                     datetime.datetime(2015, 10, 20, 1,  40, 20, 231),
                     datetime.datetime(2015, 10, 20, 1,  45, 20, 100),
                     datetime.datetime(2015, 10, 20, 1,  54, 20, 789)]
        ideal_idx = [datetime.datetime(2015, 10, 20, 1,  15),
                     datetime.datetime(2015, 10, 20, 1,  30),
                     datetime.datetime(2015, 10, 20, 1,  45)]
        test_series = pd.Series([75, 86, 91, 89, 105], index=start_idx,
                                name='test')
        ideal_series = pd.Series([75, 86, 89], index=ideal_idx,
                                 name='test').tz_localize(pytz.utc)
        self.assertTrue(utils.align_idx(test_series, 15).equals(ideal_series))


    def test_incremental_trapz(self):
        y, x = [5, 4, 9], [0, 1 ,3]
        self.assertTrue(([0.0, 4.5, 17.5], 17.5) == utils.incremental_trapz(y,
                                                                            x))


    def _gen_ts(self, begin, end, gran):
        test_idx = pd.DatetimeIndex(start=begin, end=end, freq="%dmin" % gran)
        return pd.Series(data=np.random.rand(test_idx.size), index=test_idx)


    def test_gen_data_availability_dates(self):
        gran = 15
        test_ts = self._gen_ts(datetime.datetime(2016, 1, 1, 2, 30),
                               datetime.datetime(2016, 1, 2, 19),
                               gran)
        self.assertTrue({datetime.date(2016, 1, 1)} ==
                        utils.get_data_availability_dates(test_ts, gran))


    def test_gen_bmark_readings_list(self):
        gran = 15
        bench_dt = datetime.date(2016, 1, 1)
        test_idx = pd.DatetimeIndex(start=datetime.datetime.combine(bench_dt,
                                                        datetime.time(2, 30)),
                                    end  =datetime.datetime.combine(bench_dt,
                                                        datetime.time(4, 45)),
                                    freq ="%dmin" % gran)

        data = [5, 4, 7, 1, 2, 0, 3, 6, 8, 10]
        auc  = [3, 6, 8, 11, 15, 21, 22, 27, 29, 30]
        tzone = pytz.timezone('US/Central')
        base_dt = datetime.date(2016, 2, 2)

        test_ts = pd.Series(data=data,
                            index=map(lambda x: x.time(),
                                      test_idx.to_datetime()))
        readings = utils.gen_bmark_readings_list(test_ts, auc, base_dt, tzone)

        for t in readings:
            tm, val, daily = t['time'], t['value'], t['daily']
            tm_central = tm.astimezone(tzone)
            idx = data.index(test_ts.loc[tm_central.time()])
            self.assertTrue(data[idx] == val)
            self.assertTrue(auc[idx] == daily)



if __name__ == '__main__':
    unittest.main()
