# coding=utf-8


__author__ = 'David Karapetyan'

import datetime

import pandas as pd

from larkin.model_config import model_config


def is_discrete(df, nary_thresh):
    if df.nunique() < nary_thresh:
        return True
    else:
        return False


def munge(df, nary_thresh, gap_threshold, accuracy, gran):
    """For cleaning incoming data, and extracting relevant fields

    :param df: pd.Dataframe
    :param nary_thresh: int. Number of non-unique entries before
    time series is classed as continuous
    :param gap_threshold: int. Length of data gap (in hours) we are
    allowed to interpolate over
    :param accuracy: String. Resampling fineness, relative to the original data.
    For example, "10:16:00 -> 10:15:00" would be a resampling accuracy of
    1min
    :param gran: Resampling granularity. For converting data to final
    resampling rate

    :return: pd.DataFrame. Original DataFrame, interpolated over and resampled,
     with the exception
    """
    # subset out relevant columns

    longest_allowed_gap = datetime.timedelta(hours=gap_threshold)

    # find dates with gaps less than threshold, and resample
    dates_less_thresh = df.index[
        (df.index - df.index.shift()) <= longest_allowed_gap]

    if (len(dates_less_thresh) / len(df.index)) < 0.5:
        raise ValueError("Investigate the data: it has too many gaps")

    dates_le_resamp = dates_less_thresh.resample(accuracy)

    # resampling step, where we are careful to only fill NAs via interpolation
    # for gaps less than threshold. Process nary data different than
    # continuous data

    if is_discrete(df, nary_thresh):
        df_thresh = df.resample(accuracy).fillna(method="pad")[dates_le_resamp]
    else:
        df_thresh = df.resample(accuracy).interpolate()[dates_le_resamp]

    # resample at granularity, and interpolate to fill
    # possible NAs (all of which
    # will again have gaps less than threshold

    df_thresh_gran = df_thresh.resample(gran)

    return df_thresh_gran


def ts_day_pos(ts, day, time, start, end, freq):
    """Returns slice of input time series

    Time series subset consists of all points at a specific time between
    start and end dates, and sampled with an input frequency

    :param ts: pandas.core.series.Series
    :param day: int
    Day of week
    :param time: datetime.datetime
    Time of day. Defaults to None
    :param start: datetime.datetime
    :param end: datetime.datetime
    :param freq: frequency alias
    :return: pandas.core.series.Series
    """
    temp = ts[pd.date_range(start=start, end=end, freq=freq)]
    temp = temp[temp.index.weekday == day]

    if time is None:
        return temp
    else:
        return temp.at_time(time)


def filter_two_std(ts):
    stats = ts.describe(percentiles=[.05, .95])
    low, high = stats['5%'], stats['95%']
    return ts[ts.between(low, high)]


def filter_day_season(ts, day=pd.datetime.today().weekday(),
                      month=pd.datetime.today().month):
    seasons = model_config["weather"]["seasons"]
    month_range = (0, 0)

    for value in seasons.values():
        if value[0] % 12 < month <= value[1] % 12:
            month_range = value

    # filter by day and season
    ts_filt = ts[((ts.index.weekday == day) &
                  (ts.index.month > month_range[0] % 12) &
                  (ts.index.month <= month_range[1] % 12)
                  )]
    return ts_filt
