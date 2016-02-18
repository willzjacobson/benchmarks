# coding=utf-8

__author__ = 'ashishgagneja'

import unittest
import datetime

import pytz
import pandas as pd

import nikral.benchmarks.utils as utils


class TestBmarkUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.holidays = utils.gen_holidays(datetime.date(2012, 1, 1),
                                          datetime.date(datetime.date.today().year,
                                                        12, 31),
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
        pass



if __name__ == '__main__':
    unittest.main()
