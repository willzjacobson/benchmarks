# coding=utf-8
import datetime

import dateutil.parser
import numpy

__author__ = 'David Karapetyan'

import pandas as pd
import config


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

    if df.nunique() < nary_thresh:
        df_thresh = df.resample(accuracy).fillna(method="pad")[dates_le_resamp]
    else:
        df_thresh = df.resample(accuracy).interpolate()[dates_le_resamp]

    # resample at granularity, and interpolate to fill
    # possible NAs (all of which
    # will again have gaps less than threshold

    df_thresh_gran = df_thresh.resample(gran)

    return df_thresh_gran



def _parse_tstamp(tstamp, drop_tz):
    """
    parse timestamp from database
    sample input "2015-09-21T19:45:00-04:00"

    :param tstamp: string
        timestamp as string
    :param drop_tz: bool
        flag to indicate whether to ignore/drop timezone information

    :return: datetime.datetime
    """
    if type(tstamp) == int:
        return numpy.nan
    return dateutil.parser.parse(tstamp, ignoretz=drop_tz)
    # return datetime.datetime.strptime(tstamp, "%Y-%m-%dT%H:%M:%S%z")


def convert_datatypes(ts_list, value_list, drop_tz=True, val_type=float):
    """
    Parse timestamp and observation data read from database. Timestamps
    are converted to datetime.datetime ignoring timezone information.
    Observations are cast to val_type

    :param ts_list: list
        list of timestamps
    :param value_list: list
        list of observations
    :param drop_tz: bool
        flag to indicate whether to ignore timezone information
    :param val_type: function
        function to use to cast observation to the required type
        If None, no transformation is done

    :return: list of lists
        list containing a list with parsed timestamps followed by another one
        with transformed/casted observation data

    """

    # parse timestamps to datetime and drop timezone
    # placeholder readings could have '0' as time, replace with NaN
    # ts_list = joblib.Parallel(n_jobs=2)(joblib.delayed(
    #     _parse_tstamp)(x, drop_tz) for x in ts_list)

    ts_list = list(map(lambda x: dateutil.parser.parse(
            x, ignoretz=drop_tz) if type(x) is not int else numpy.nan, ts_list))

    # convert str to val_type
    if val_type:
        # value_list = list(map(val_type, value_list))
        # print(numpy.asarray(value_list)[:100])

        arr = numpy.asarray(value_list)
        if val_type == float:
            value_list = arr.astype(numpy.float)
        elif val_type == int:
            value_list = arr.astype(numpy.int64)
        else:
            raise Exception('unsupported transformation')

    return [ts_list, value_list]


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
    seasons = config.david["building_dbs"]["seasons"]
    month_range = (0, 0)

    for value in seasons.values():
        if value[0] < month <= value[1]:
            month_range = value

    # filter by day and season
    ts_filt = ts[((ts.index.weekday == day) &
                  (ts.index.month > month_range[0]) &
                  (ts.index.month <= month_range[1])
                  )]
    return ts_filt
