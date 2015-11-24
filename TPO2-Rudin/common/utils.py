__author__ = 'ashishgagneja'

import dateutil.parser
import numpy
import datetime
import pandas as pd
import db.connect as connect
import math



def dow_type(dt):

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
        device name for time series
    :param system: string
        system name for time series
    :param field: string
        field name for time series

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

    # find index overlap
    common_tms = set(gold_ts.index).intersection(set(other_ts.index))

    # if index overlap is less than threshold, do not compute score
    if len(common_tms) < 0.95 * gold_ts.size:
        # print('data overlap below threshold: %s' % other_ts.index[0].date())
        return None

    norm_ts = gold_ts.loc[common_tms] - other_ts.loc[common_tms]
    # L2 norm is normalized by number of overlapping keys to make sure days with
    # more overlapping data available are not at a disadvantage
    return math.sqrt((norm_ts**2).sum()/len(common_tms))



def find_similar_profile_days(gold_ts, gold_dow_type, all_ts, k, data_avlblty):

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
        list containing two lists: parsed timestamps followed by transformed
        observation data

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
    bod_tm = datetime.time(0, 0, 0, 0)
    start_idx = datetime.datetime.combine(dt, bod_tm)
    end_idx = datetime.datetime.combine(
        dt + dateutil.relativedelta.relativedelta(days=1), bod_tm)
    return full_ts[str(start_idx) : str(end_idx)]
