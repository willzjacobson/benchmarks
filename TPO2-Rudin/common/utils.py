__author__ = 'ashishgagneja'

import dateutil.parser
import numpy



def find_similar_profile_days(gold_ts, all_ts, k, data_avlblty):

    # find long list of dates
    all_dates = list(all_ts.index.date)

    # find cutoff date
    cutoff_dt = gold_ts.index[0].to_datetime().date()
    print("cutoff date: %s" % cutoff_dt)

    all_dates = [t for t in all_dates if t < cutoff_dt]

    # compute similarity score for each date

    # return the top k scores and corresponding dates



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