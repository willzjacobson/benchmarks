# coding: utf-8
# from IPython.parallel import Client
# rc=Client()
import pandas as pd


def data_clean(data, title):
    """For cleaning BMS data, and extracting relevant fields

    :param data: Dataframe
    :param title: String
    :return: Series
    """
    # subset out relevant columns
    data.columns = ['ID', 'TIMESTAMP',
                    'TRENDFLAGS', 'STATUS',
                    'VALUE', 'TRENDFLAGS_TAG',
                    'STATUS_TAG']
    data = data.sort('TIMESTAMP')

    # construct time series, getting rid of microseconds
    ts = pd.Series(list(data.VALUE),
                   pd.DatetimeIndex(data.TIMESTAMP),
                   name=title)

    ts = ts.resample('15Min')

    return ts
