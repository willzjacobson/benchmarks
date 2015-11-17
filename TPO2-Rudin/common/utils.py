__author__ = 'ashishgagneja'

import dateutil.parser
import numpy


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