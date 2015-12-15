# coding=utf-8
import datetime
import dateutil.parser
import numpy

__author__ = 'David Karapetyan'

import pandas as pd
import pandas.tseries.offsets as offsets

import config


def _find_longest_gap(index):
    """ Find longest gap length in hours
    :param index: pandas.DatetimeIndex
        contains all available indices
    :return: pandas.tslib.Timedelta
    """

    df = pd.DataFrame(data=index, columns=['ts'])
    df['diff'] = (df['ts'] - df['ts'].shift()).fillna(0)
    return df.max(axis=0)['diff']


def _is_resamplable(ts_index, max_gap):
    """ Determines if a timeseries is missing too much data for resampling to
        be counter-productive. Gaps longer than a few hours cause modelling
        problems

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

    # TODO: dropping duplicates based on timestamp alone could result in lost
    # data if the data has readings from more than one meter/equipment
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


def filter_day_season(ts, day=pd.datetime.today().weekday(),
                      month=pd.datetime.today().month):
    seasons = config.david["weather"]["seasons"]
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


def _clear_sec_musec(tstamp):
    """
    clear second and microsecond fields of timestamp

    :param tstamp: timestamp like object
    :return: timestamp like object
    """

    tstamp -= datetime.timedelta(seconds=tstamp.second,
                                 microseconds=tstamp.microsecond)
    return tstamp


def _round_minute(tstamp, gran, is_begin_data):
    """
    find the closest regularized timestamp. if is_begin_data is True, looks
    forward, otherwise looks backward

    For example: tstamp = '2015-11-22T15:21:05', gran = 15
        if is_begin_data is True, returns '2015-11-22T15:30:00', otherwise
        returns '2015-11-22T15:15:00'

    :param tstamp: timestamp like object
    :param gran: int
        expected frequency of observations and forecast in minutes
    :param is_begin_data: bool
        True if tstamp is from the first available observation, False otherwise
    :return:
    """
    one_minute = datetime.timedelta(minutes=1)
    max_tries = 60

    count = 0
    tmp_tstamp = tstamp
    while tmp_tstamp.minute % gran != 0:
        if is_begin_data:
            tmp_tstamp += one_minute
        else:
            tmp_tstamp -= one_minute

        count += 1
        if count > max_tries:
            raise Exception("failure rounding timestamp <%s>" % tstamp)

    return _clear_sec_musec(tmp_tstamp)


def _round_tstamp(tstamp, gran, is_begin_data=True):
    """
    round timestamp to closest regularized value in the direction dictated by
    is_begin_data. If True, normalize forward, otherwise backward


    :param tstamp: timestamp like object
    :param gran: int
        expected frequency of observations and forecast in minutes
    :param is_begin_data: bool
        True if tstamp is from the first available observation, False otherwise
    :return:
    """

    if not _is_tstamp_rounded(tstamp, gran):
        return _round_minute(_clear_sec_musec(tstamp), gran, is_begin_data)
    return tstamp


def _is_tstamp_rounded(tstamp, gran):
    """
    check if timestamp is rounded/regularized

    :param tstamp: datetime like object
    :param gran: int
        expected frequency of observations and forecast in minutes

    :return: bool
    """
    if (tstamp.minute % gran == 0 and tstamp.second == 0 and
                tstamp.microsecond == 0):
        return True
    return False


def _find_gaps(index, threshold):
    """
    find gaps in index longer than threshold hours

    :param index: pandas DatetimeIndex
        index to operate one
    :param threshold: int
        length of longest permissible gap in the index in hours

    :return: pandas DataFrame
        Has columns ['begin', 'end', 'diff']
        Each row represents interval (row['begin'], row['end'])
        The interval end point is open/closed depending upon whether or not the
        specific timestamp is rounded/regularized.
    """

    df = pd.DataFrame(data=index, columns=['end'])
    df['begin'] = df['end'].shift()
    df['diff'] = (df['end'] - df['begin']).fillna(0)
    longest_allowed_gap = datetime.timedelta(hours=threshold)
    return df[df['diff'] > longest_allowed_gap]


def _drop_large_gaps(index, gap_info, gran):
    """
    remove gaps from timestamp index
    gaps are first consolidated into one DatetimeIndex and then dropped from
    the main index for efficiency

    :param index: pandas DatetimeIndex
    :param gap_info: pandas DataFrame
        gap information with columns begin, end and diff
    :param gran: int
        expected frequency of observations and forecast in minutes
    :return:
    """

    to_drop = None
    freq = "%dmin" % gran

    interval = datetime.timedelta(minutes=gran)
    for _, row in gap_info.iterrows():

        start_ts = (row['begin'] + interval
                    if _is_tstamp_rounded(row['begin'], gran)
                    else row['begin'])
        end_ts   = (row['end']   - interval
                    if _is_tstamp_rounded(row['end'], gran)
                    else row['end'])

        if end_ts - start_ts > interval:
            # we have an open interval
            sub_idx = pd.DatetimeIndex(start=start_ts, end=end_ts, freq=freq)
            to_drop = to_drop.union(sub_idx) if to_drop is not None else sub_idx

    return index.difference(to_drop) if to_drop is not None else index


def _get_ideal_index(index, gran):
    """
    generate best possible index with gran as frequency that can be obtained
    index-snippets from gaps longer than two hours are trimmed
    Assumption: No NAs in the data

    :param index: pandas DatetimeIndex
        timestamp-based index of available data
    :param gran: int
        expected frequency of observations and forecast in minutes

    :return: pandas DatetimeIndex
    """
    ideal_index = pd.DatetimeIndex(start=_round_tstamp(index[0], gran),
                                   end=_round_tstamp(index[-1], gran, False),
                                   freq="%dmin" % gran)
    return _drop_large_gaps(ideal_index, _find_gaps(index, 2), gran)


def interp_tseries(tseries, gran):
    """
    interpolate time series data using linear interpolation to fill missing data
    data gaps longer than 2 hours are ignored

    :param tseries: pandas Series or DataFrame
        time series data to interpolate
    :param gran: int
        expected frequency of observations and forecast in minutes

    :return: pandas Series or DataFrame
    """

    ideal_index = _get_ideal_index(tseries.index, gran)
    # this approach does not work for some reason, the reindex takes forever
    # full_index = ideal_index.union(tseries.index)
    # full_tseries = tseries.reindex(full_index)

    # limit does not seem to work when method is specified as time
    return tseries.resample('5T', how='median').interpolate(
        method='time').reindex(ideal_index)


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
        #value_list = list(map(val_type, value_list))
        # print(numpy.asarray(value_list)[:100])

        arr = numpy.asarray(value_list)
        if val_type == float:
            value_list = arr.astype(numpy.float)
        elif val_type == int:
            value_list = arr.astype(numpy.int64)
        else:
            raise Exception('unsupported transformation')

    return [ts_list, value_list]