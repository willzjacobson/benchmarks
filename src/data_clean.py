# coding: utf-8
# from IPython.parallel import Client
# rc=Client()
import os

import pandas as pd


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


def csv_dir_to_hdf(path_to_dir="/", header=0, sep="\,"):
    for root, dirs, files in os.walk(path_to_dir):

        store = pd.HDFStore(root + ".h5")

        for file in files:
            # store name of file, without extension
            storage_name = os.path.splitext(file)[0]

            store[storage_name] = pd.read_csv(
                root + "/" + file, header=header, sep=sep)

        store.close()


def csv_multicsv_to_hdf(path_to_dir, header=0, sep="\,"):
    master, sorted_csvs, store = pd.DataFrame(), None, None

    for root, dirs, files in os.walk(path_to_dir):
        store = pd.HDFStore(root + ".h5")

        for file in files:

            temp = pd.read_csv(root + "/" + file, header=header, sep=sep)

            if file.count("_") < 2:
                string_split = file.split("_", file.count("_"))
                controller = string_split[0]
                subcontroller = string_split[1]
                pointname = string_split[2]
            else:
                string_split = file.split("_", 1)
                controller = string_split[0]
                subcontroller = float('NaN')
                pointname = string_split[1]


            # add new columns
            temp.insert(0, 'Controller', controller)
            temp.insert(1, 'SubController', subcontroller)
            temp.insert(2, 'PointName', pointname)

            master = pd.concat([master, temp])

    store['df'] = master
    store.close()
