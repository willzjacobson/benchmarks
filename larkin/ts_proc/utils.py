# coding=utf-8
# import IPython.parallel

# rc = IPython.parallel.Client()
# dview = rc[:]
# dview.block = True

# with dview.sync_imports():
import pymongo

# from statsmodels.tsa.statespace.sarimax import SARIMAX
# import seaborn as sns
import pandas as pd
import joblib
# sns.set()
import pytz


def _construct_electric_dataframe(ts_lists, value_lists):
    """
    Construct a pandas DataFrame using the time series data on individual
    meter can compute the total instantaneous usage

    :param ts_lists: list of lists
        list of list of timestamps
    :param value_lists: list of lists
        list of list of data corresponding to the timestamps list in the same
        ordinal position in ts_lists

    :return:
    """

    master_df = pd.DataFrame()

    # error checks
    if len(ts_lists) != len(value_lists):
        raise ValueError('array lengths must match')
    if not len(ts_lists):
        return master_df


    # insert column data
    for i, ts_list in enumerate(ts_lists):
        master_df = master_df.join(pd.DataFrame(data=value_lists[i],
                                                index=ts_list,
                                                columns=[str(i + 1)]).dropna(),
                                   how='outer')

    return master_df.sum(axis=1).sort_index()


def get_electric_ts(host, port, database, username, password, source,
                    collection_name, building, meter_count):
    """ retrieves all available electric data from all meters and sums up
    to get total electric usage time series

    :param host: string
        database server name or IP-address
    :param port: int
        database port number
    :param database: string
        name of the database on server
    :param username: string
        database username
    :param password: string
        database password
    :param source: string
        source database for authentication
    :param collection_name: string
        database collection name to query
    :param building: string
        database building_id identifier
    :param meter_count: int
        number of distinct meters that need to be summed up

    :return: pandas Dataframe
    """

    results = joblib.Parallel(n_jobs=-1)(joblib.delayed(get_ts_new_schema)(
                        host, port, database, username, password, source,
                        collection_name, building,
                        "Elec-M%d" % equip_id, 'SIF_Electric_Demand')
                                    for equip_id in range(1, meter_count + 1))

    ts_lists, value_lists = zip(*results)

    return _construct_electric_dataframe(ts_lists, value_lists).tz_localize(
                                                                       pytz.utc)


def get_parsed_ts_new_schema(host, port, db_name, username, password,
                             source, collection_name, building, device,
                             system=None, floor=None, quad=None):
    """Fetch all available timeseries data from database

    :param host: string
        database server name or IP-address
    :param port: int
        database port number
    :param db_name: string
        name of the database on server
    :param username: string
        database username
    :param password: string
        database password
    :param source: string
        source database for authentication
    :param collection_name: string
        collection name to use
    :param building: string
        building identifier
    :param device: string
        device name for identifying time series
    :param system: string
        system name for identifying time series
    :param floor: string
        floor identifier
    :param quad: string
        quadrant identifier

    :return: pandas DataFrame
        occupancy time series data
    """


    ts_list, val_list = get_ts_new_schema(host, port, db_name, username,
                                          password, source, collection_name,
                                          building, device, system, floor=floor,
                                          quad=quad)

    obs_df = pd.DataFrame({'obs': val_list}, index=ts_list).dropna()

    # drop missing values, set timestamp as the new index and sort by index
    # some duplicates seen in SIF steam data
    return obs_df.sort_index().tz_localize(pytz.utc)['obs']


def get_ts_new_schema(host, port, database, username, password, source,
                      collection_name, building, device, system=None,
                      floor=None, quad=None):
    """
    Get all observation data with the given building, device and system
    combination from the database

    :param host: string
        database server name or IP-address
    :param port: int
        database port number
    :param database: string
        name of the database on server
    :param username: string
        database username
    :param password: string
        database password
    :param source: string
        source database for authentication
    :param collection_name: string
        database collection name
    :param building: string
        building identifier
    :param device: string
        device name for identifying time series
    :param system: string
        system name for identifying time series
    :param floor: string
        floor identifier
    :param quad: string
        quadrant identifier

    :return: tuple with a list of time stamps followed by a list of values
    """

    with pymongo.MongoClient(host, port) as conn:

        conn[database].authenticate(username, password, source=source)
        collection = conn[database][collection_name]

        ts_list, value_list = [], []

        query = {'building': building,
                 'device'  : device}

        # handle optional arguments
        for field, value in {'system': system, 'floor': floor,
                             'quadrant': quad}.iteritems():
            if value is not None:
                query[field] = value

        for data in collection.find(query):

            readings = data['readings']
            zipped = [(x['time'], x['value']) for x in readings
                                      if x['time'] is not None and 'value' in x]

            if len(zipped):
                ts_list_t, val_list_t = zip(*zipped)
                ts_list.extend(ts_list_t)
                value_list.extend(val_list_t)

    return ts_list, value_list


