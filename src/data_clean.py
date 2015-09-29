# coding: utf-8
# from IPython.parallel import Client
# rc=Client()
import pandas as pd
import os


def data_clean_park(data, title):
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




def csv_dir_to_hdf(path_to_dir, header=0, sep="\,"):
    for root, dirs, files in os.walk(path_to_dir):

        sorted_csvs = files
        sorted_csvs.sort()

        store = pd.HDFStore(root + ".h5")

        for file in sorted_csvs:
            # store name of file, without extension
            storage_name = os.path.splitext(file)[0]

            store[storage_name] = pd.read_csv(
                root + "/" + file, header=header, sep=sep)

    store.close()
