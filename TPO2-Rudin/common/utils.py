__author__ = 'ashishgagneja'

import dateutil.parser
import numpy
import datetime
import pandas as pd
import db.connect as connect
import math
import joblib



def dow_type(dt):
    """
    Find day of week type.
    Type 1: Mondays are usually different from other weekdays
    Type 2:Tue-Thu are categorized as one type
    Type 3: Fridays are different from other days as some people leave early
    Type 4: weekend has it
    own type

    :param dt: datetime.date
    :return: int in [1, 2, 3, 4]
    """

    dow = dt.isoweekday()

    if dow in [1]: # Monday
        return 1
    elif dow in [2, 3, 4]: # Tue, Wed, Thu
        return 2
    elif dow in [5]: # Friday
        return 3
    else: # weekend
        return 4


def drop_series_ix_date(tseries):
    """
    Drop dates from Series index

    :param tseries: pandas Series of DataFrame
        Data set to work on
    :return: pandas Series
    """
    return pd.Series(data=tseries.data, index=map(lambda x: x.time(),
                                                  tseries.index.to_datetime()))



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



def get_ts(db_server, db_name, collection_name, bldg_id, device, system, field):
    """
    Get all observation data with the given building, device and system
    combination from the database

    :param db_server: string
        database server name or IP-address
    :param db_name: string
        name of the database on server
    :param collection_name: string
        collection name to use
    :param bldg_id: string
        building identifier
    :param device: string
        device name for identifying time series
    :param system: string
        system name for identifying time series
    :param field: string
        field name for identifying time series

    :return: tuple with a list of time stamps followed by a list of values
    """


    with connect.connect(db_server, database=db_name) as conn:

        collection = conn[db_name][collection_name]

        ts_list, value_list, daily_dict = [], [], {}
        for data in collection.find({"_id.building": bldg_id,
                                     "_id.device": device,
                                     "_id.system": system}):

            readings = data['readings']
            zipped = map(lambda x: (x['time'], x[field]), readings)

            ts_list_t, val_list_t = zip(*zipped)

            ts_list.extend(ts_list_t)
            value_list.extend(val_list_t)

    return ts_list, value_list



def compute_profile_similarity_score(gold_ts, other_ts):
    """
    compute similarity score of two profiles/time-series snippets
    Similarity score is the L2 norm computed using values associated with
    indices common to both profiles. The score is normalized by number of common
    indices to avoid penalizing days with larger overlaps

    Assumption: Index over must be 90% or more

    :param gold_ts: pandas Series
        time series from base date
    :param other_ts: pandas Series
        time series from another past day

    :return: float
    """

    # find index overlap
    common_tms = set(gold_ts.index).intersection(set(other_ts.index))

    # if index overlap is less than threshold, do not compute score
    if len(common_tms) < 0.90 * gold_ts.size:
        # print('data overlap below threshold: %s' % other_ts.index[0].date())
        return None

    norm_ts = gold_ts.loc[common_tms] - other_ts.loc[common_tms]
    # L2 norm is normalized by number of overlapping keys to make sure days with
    # more overlapping data available are not at a disadvantage
    return math.sqrt((norm_ts**2).sum()/len(common_tms))



def find_similar_profile_days(gold_ts, gold_dow_type, all_ts, k, data_avlblty):
    """
    Find k most similar profile days within all_ts with day-of-week type
    matching gold_dow_type and profile/time-series most similar to gold_ts such
    that they are also in the set data_avlblty

    :param gold_ts: pandas Series
        base time series
    :param gold_dow_type: int
        day-of-week type for base date
    :param all_ts: pandas Series
        complete time series to search similar profile days in
    :param k: int
        number of most similar days to returns
    :param data_avlblty: set
        set of dates which must contain the k most similar days selected

    :return: list of top k dates with most similar profiles
    """

    # find long list of dates
    all_dates = list(all_ts.index.date)

    # find cutoff date
    cutoff_dt = gold_ts.index[0].to_datetime().date()
    # print("cutoff date: %s" % cutoff_dt)

    # drop future dates and dates from other day of week types
    all_dates = set([t for t in all_dates if t < cutoff_dt and
                     dow_type(t) == gold_dow_type])

    # compute similarity score for each date
    one_day = datetime.timedelta(days=1)
    gold_ts_nodate = drop_series_ix_date(gold_ts)
    sim_scores = []
    for dt in all_dates:

        if dt in data_avlblty:

            end_idx = datetime.datetime.combine(dt + one_day, datetime.time.min)
            score = compute_profile_similarity_score(gold_ts_nodate,
                        drop_series_ix_date(all_ts[dt: end_idx]))

            if score:
                sim_scores.append([dt, score])

    # return the top k closest dates; smaller scores are better
    keys, _ = zip(*sorted(sim_scores, key=lambda x: x[1]))
    return keys[:k]



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
    :param drop_tz (optional): bool
        flag to indicate whether to ignore timezone information
    :param val_type (optional): function
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



def get_dt_tseries(dt, full_ts):
    """
    Get time series snippet for the given date

    :param dt: datetime.date
        Date for which to get the observation data from
    :param full_ts: pandas Series or DataFrame
        complete observation / time series data set

    :return: pandas Series or DataFrame
    """
    start_idx = datetime.datetime.combine(dt, datetime.time.min)
    end_idx = datetime.datetime.combine(dt, datetime.time.max)
    return full_ts[str(start_idx) : str(end_idx)]



def debug_msg(debug, str):
    """
    print debug message to log or stdout if debug is True
    :param debug: bool
    :param str: string
        debug message
    :return:
    """
    if debug:
        print(str)



def gen_readings_list(tseries):
    """
    generate list of readings with each item being a dictionary of the form:
    {"time": <datetime/date/time>, "value": <value>}

    :param tseries: pandas Series
        time series snippet to
    :return: list
    """

    return [{'time': str(ix), 'value': val} for ix, val in tseries.iteritems()]