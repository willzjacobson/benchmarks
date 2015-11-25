__author__ = 'ashishgagneja'

import dateutil.parser
import numpy
import datetime
import pandas as pd
import db.connect as connect
import math



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
    print("cutoff date: %s" % cutoff_dt)

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

    # parse timestamps to dateime and drop timezone
    # placeholder readings could have '0' as time, replace with NaN
    ts_list = list(map(lambda x: dateutil.parser.parse(
        x, ignoretz=drop_tz) if type(x) is not int else numpy.nan, ts_list))

    # convert str to val_type
    if val_type:
        value_list = list(map(val_type, value_list))

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



def gen_readings_list(tseries):
    """
    generate list of readings with each item being a dictionary of the form:
    {"time": <datetime/date/time>, "value": <value>}

    :param tseries: pandas Series
        time series snippet to
    :return: list
    """

    return [{'time': str(ix), 'value': val} for ix, val in tseries.iteritems()]