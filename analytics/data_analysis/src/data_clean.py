# coding: utf-8
# from IPython.parallel import Client
# rc=Client()
import os
from joblib import Parallel, delayed
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


def _split_concat(file, root, sep="|"):
    print(file)
    temp = pd.read_csv(root + "/" + file,
                       header=None,
                       sep=sep,
                       dtype="object")

    if file.count("_") > 1:
        string_split = file.split("_", 2)
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
    return temp


def csv_dir_to_hdf(path_to_dir="/", header=0, sep="\,"):
    for root, dirs, files in os.walk(path_to_dir):

        store = pd.HDFStore(root + ".h5")

        for file in files:
            # store name of file, without extension
            storage_name = os.path.splitext(file)[0]

            store[storage_name] = pd.read_csv(
                root + "/" + file, header=header, sep=sep)

        store.close()


def csv_multicsv_to_hdf(path_to_dir, sep="|"):
    root, dirs, files = list(os.walk(path_to_dir))[0][0:3]
    store = pd.HDFStore(root + ".h5")

    frames = (Parallel(n_jobs=-1, verbose=51)(delayed(_split_concat)(file, root, sep)
                                  for file in files))

    # master = pd.concat(frames, verify_integrity=True)
    # store['df'] = master
    # store.close()
    return frames
