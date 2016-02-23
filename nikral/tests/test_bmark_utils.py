# coding=utf-8

__author__ = 'ashishgagneja'

import unittest
import datetime

import pytz

import pandas as pd

import numpy as np

import nikral.benchmarks.utils as utils
import nikral.shared.utils as shr_utils


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


    def _gen_ts(self, begin, end, gran, data=None):
        test_idx = pd.DatetimeIndex(start=begin, end=end, freq="%dmin" % gran)
        return pd.Series(data=data if data else np.random.choice(range(1, 9),
                                                            size=test_idx.size),
                         index=test_idx)


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


    def test_find_similar_occ_day(self):

        start_dt, end_dt = datetime.date(2014, 2, 1), datetime.date(2015, 10, 2)

        occ_availability = [end_dt - datetime.timedelta(days=x)
                            for x in range(0, 600)]

        # holidays = utils.gen_holidays(start_dt, end_dt, '345_Park')

        tmp_dt = start_dt + datetime.timedelta(days=365)
        one_day = datetime.timedelta(days=1)
        while tmp_dt < end_dt:

            tmp_sim_occ_dt = utils.find_similar_occ_day(tmp_dt,
                                                        occ_availability,
                                                        self.holidays)
            self.assertTrue(tmp_sim_occ_dt is not None)

            tmp_sim_occ_dt_is_hol = utils.is_holiday(tmp_sim_occ_dt,
                                                     self.holidays)

            self.assertTrue(tmp_sim_occ_dt < tmp_dt)
            self.assertTrue(utils.is_holiday(tmp_dt, self.holidays)
                            == tmp_sim_occ_dt_is_hol)
            if not tmp_sim_occ_dt_is_hol:
                self.assertTrue(shr_utils.dow_type(tmp_dt)
                                == shr_utils.dow_type(tmp_sim_occ_dt))

            tmp_dt += one_day


    def test_find_lowest_auc_day(self):
        tzone = pytz.timezone('US/Central')
        dt1, dt2 = datetime.date(2015, 12, 20), datetime.date(2014, 12, 12)
        dt_scores = [(dt2, 19.762), (dt1, 22.43)]
        one_day = datetime.timedelta(days=1)

        test_ts1 = self._gen_ts(datetime.datetime.combine(dt1,
                                                          datetime.time(6)),
                                datetime.datetime.combine(dt1 + one_day,
                                                          datetime.time(6)),
                                180, [58, 43, 35, 43, 64, 87, 86, 63, 69]
                                ).tz_localize(pytz.utc).tz_convert(tzone)
        test_ts2 = self._gen_ts(datetime.datetime.combine(dt2,
                                                          datetime.time(6)),
                                datetime.datetime.combine(dt2 + one_day,
                                                          datetime.time(6)),
                                180, [72, 40, 39, 47, 69, 88, 77, 70, 77]
                                ).tz_localize(pytz.utc).tz_convert(tzone)
        test_ts = pd.concat([test_ts2, test_ts1])
        result = utils.find_lowest_auc_day(dt_scores, test_ts, 2, tzone, False)
        self.assertTrue(result[0] == dt1)
        self.assertTrue(1255 < result[1] < 1256)
        self.assertTrue(isinstance(result[2], list))
        self.assertTrue(1255 < result[2][-1] < 1256)
        self.assertTrue(len(result[2]) == 8)
        self.assertTrue(isinstance(result[3], pd.Series))



if __name__ == '__main__':
    unittest.main()
