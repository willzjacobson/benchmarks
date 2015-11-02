__author__ = 'davidkarapetyan'

import pandas as pd
import config
import numpy as np

def _find_longest_gap(diff_index, granularity):
    """ Find longest gap length in hours
    :param diff_index: pandas.DatetimeIndex
        contains missing indices
    ;param granularity: int
    :return: numpy.timedelta64
    """

    prev_ts, gap_begin, max_gap_duration = None, None, np.timedelta64()
    # adding 1 more minute take care of second differences which we ignore
    td = np.timedelta64(granularity + 1, 'm')

    for ts in diff_index:

        if prev_ts:

            # start of a new gap
            if ts - prev_ts > td:

                # if we are already in a gap, save duration and reset gap beginning
                if gap_begin:

                    tmp_gap_dur = prev_ts - gap_begin
                    if tmp_gap_dur > max_gap_duration:
                        max_gap_duration = tmp_gap_dur

                gap_begin = ts

        else: # first gap
            gap_begin = ts

        prev_ts = ts

    return max_gap_duration


def _is_resamplable(ts_index, granularity, max_gap):
    """ Determines if a timeseries is missing too much data for resampling to be counter-productive
        Gaps longer than a few hours cause modelling problems

    ;param ts_index: pandas.tseries.index.DatetimeIndex
        timestamp index of available data
    ;param granularity: int
        time series frequency
    ;param max_gap: int
        length, in hours, of the longest allowed hour
    :return: bool
    """

    ideal_index = pd.DatetimeIndex(freq=granularity, start=ts_index[0], end=ts_index[-1])
    diff = ideal_index.difference(ts_index)
    diff_sorted = diff.order()

    longest_allowed_gap = np.timedelta64(max_gap, 'h')
    if _find_longest_gap(diff_sorted, granularity) > longest_allowed_gap:
        return False

    return True



def munge(data, title=None):
    """For cleaning incoming data, and extracting relevant fields

    :param data: Dataframe
    :param title: String
    :return: Series
    """
    # subset out relevant columns
    data = data.sort('TIMESTAMP')

    # construct time series, getting rid of microseconds
    ts = pd.Series(list(data.VALUE),
                   pd.DatetimeIndex(data.TIMESTAMP),
                   name=title)
    gran = str(config.david["sampling"]["granularity"]) + "min"

    # TODO: dropping duplicates based on timestamp alone could result in lost data if the data has readings from
    # more than one meter/equipment
    if not _is_resamplable(ts.keys(), int(gran), config.ashish["sampling"]["max_gap"]):
        raise Exception("data gap longer than threshold encountered")

    ts = ts.drop_duplicates(subset="TIMESTAMP").resample(gran)

    # identify if time series is nary, or continuous, and process
    # accordingly

    nary_thresh = config.david["sampling"]["nary_thresh"]
    if ts.nunique() < nary_thresh:
        ts = ts.fillna(method="pad")
    else:
        ts = ts.interpolate(method="linear")

    return ts
