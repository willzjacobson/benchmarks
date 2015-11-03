__author__ = 'davidkarapetyan'

import pandas as pd
import pandas.tseries.offsets as offsets

import config


def _find_longest_gap(index):
    """ Find longest gap length in hours
    :param index: pandas.DatetimeIndex
        contains all available indices
    :return: pandas.tslib.Timedelta
    """

    prev_ts, max_gap_duration = None, pd.Timedelta(offsets.Second(0))

    for ts in index:

        if prev_ts:

            tmp_gap = ts - prev_ts
            if tmp_gap > max_gap_duration:
                print('gap found: %s - %s' % (prev_ts, ts))
                max_gap_duration = tmp_gap

        prev_ts = ts

    return max_gap_duration



def _is_resamplable(ts_index, max_gap):
    """ Determines if a timeseries is missing too much data for resampling to be counter-productive
        Gaps longer than a few hours cause modelling problems

    ;param ts_index: pandas.tseries.index.DatetimeIndex
        timestamp index of available data
    ;param max_gap: int
        length, in hours, of the longest allowed hour
    :return: bool
    """

    longest_allowed_gap = pd.Timedelta(offsets.Hour(max_gap))
    if _find_longest_gap(ts_index) > longest_allowed_gap:
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
    if not _is_resamplable(ts.keys(), config.ashish["sampling"]["max_gap"]):
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
