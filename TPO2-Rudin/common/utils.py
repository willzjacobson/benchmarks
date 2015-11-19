__author__ = 'ashishgagneja'

import dateutil.parser
import numpy
import datetime
import pandas as pd


def _drop_series_ix_date(tseries):

    return pd.Series(data=tseries.data, index=map(lambda x: x.time(),
                                                  tseries.index.to_datetime()))


def _compute_profile_similarity_score(gold_ts, other_ts):

    # find index overlapping
    # gold_time_idx = list(map(lambda x: (x, x.time()), gold_datetimes))
    # gold_ts_reidx = gold_ts.reindex(list(map(lambda x: x.time(),
    # gold_ts_reidx = pd.Series(data=gold_ts.data, index=map(
    #     lambda x: x.time(), gold_ts.index.to_datetime()))
    # other_ts_reidx = _drop_series_ix_date(other_ts)

    common_tms = set(gold_ts.index).intersection(set(other_ts.index))

    # print("common tms: %s, %s" % (len(common_tms), common_tms))
    if len(common_tms) < 0.95 * gold_ts.size:
        # print('data overlap below threshold: %s' % other_ts.index[0].date())
        return None

    norm_ts = gold_ts.loc[common_tms] - other_ts.loc[common_tms]
    # L2 norm is normalized by number of overlapping keys to make sure days with
    # more overlapping data available are not at a disadvantage
    return (norm_ts**2).sum()/len(common_tms)



def find_similar_profile_days(gold_ts, all_ts, k, data_avlblty):

    # find long list of dates
    all_dates = list(all_ts.index.date)

    # find cutoff date
    cutoff_dt = gold_ts.index[0].to_datetime().date()
    print("cutoff date: %s" % cutoff_dt)

    all_dates = set([t for t in all_dates if t < cutoff_dt])

    # compute similarity score for each date
    one_day = datetime.timedelta(days=1)
    gold_ts_nodate = _drop_series_ix_date(gold_ts)
    sim_scores = []
    for dt in all_dates:

        if dt in data_avlblty:

            end_idx = datetime.datetime.combine(dt + one_day, datetime.time.min)
            score = _compute_profile_similarity_score(gold_ts_nodate,
                        _drop_series_ix_date(all_ts[dt: end_idx]))

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