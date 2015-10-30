__author__ = 'davidkarapetyan'

import pandas as pd
import config


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
    ts = ts.drop_duplicates(subset="TIMESTAMP").resample(gran)

    # identify if time series is nary, or continuous, and process
    # accordingly

    nary_thresh = config.david["sampling"]["nary_thresh"]
    if ts.nunique() < nary_thresh:
        ts = ts.fillna(method="pad")
    else:
        ts = ts.interpolate(method="linear")

    return ts
