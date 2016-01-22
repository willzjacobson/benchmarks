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
import datetime

#TODO: delete these import
import misc

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


    start_tm = datetime.datetime.utcnow()
    # insert column data
    for i, ts_list in enumerate(ts_lists):
        print(len(value_lists[i]))
        print(len(ts_list))
        master_df = master_df.join(pd.DataFrame(data=value_lists[i],
                                                index=ts_list,
                                                columns=[str(i + 1)]).dropna(),
                                   how='outer')

    print("df join took: %s" % misc.get_elapsed_tm(start_tm))

    return master_df.sum(axis=1).reset_index().drop_duplicates(
        subset='index').set_index('index').sort_index()


def _construct_electric_dataframe_new(ts_lists, value_lists, data):
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

    start_tm = datetime.datetime.utcnow()
    # insert column data
    for i, ts_list in enumerate(ts_lists):
        master_df = master_df.join(pd.DataFrame(data=value_lists[i],
                                                index=ts_list,
                                                columns=[str(i + 1)]).dropna(),
                                   how='outer')

    print("df join took: %s" % misc.get_elapsed_tm(start_tm))

    return master_df.sum(axis=1).reset_index().drop_duplicates(
        subset='index').set_index('index').sort_index()


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

    start_tm = datetime.datetime.utcnow()
    results = joblib.Parallel(n_jobs=-1)(joblib.delayed(get_ts_new_schema)(
                    host, port, database, username, password, source,
                    collection_name, building,
                    ["Elec-M%d" % meter_num,
                     "Electric_Meter_%d^Avg_Rate" % meter_num],
                    ['SIF_Electric_Demand', 'Electric_Utility'])
                        for meter_num in range(1, meter_count + 1))

    print("multi-thread query took: %s" % misc.get_elapsed_tm(start_tm))

    ts_lists, value_lists = zip(*results)

    start_tm = datetime.datetime.utcnow()
    ts_lists_st, value_lists_st = [], []
    for meter_num in range(1, meter_count + 1):
        ts_list_t, value_list_t = get_ts_new_schema(host, port, database,
                                                    username, password, source,
                                                    collection_name, building,
                                                    ["Elec-M%d" % meter_num,
                                                     "Electric_Meter_%d^Avg_Rate" % meter_num],
                                                    ['SIF_Electric_Demand',
                                                     'Electric_Utility'])
        ts_lists_st.append(ts_list_t)
        value_lists_st.append(value_list_t)

    print("single-thread query took: %s" % misc.get_elapsed_tm(start_tm))

    start_tm = datetime.datetime.utcnow()
    devices = []
    meter_groups = {}
    for meter_num in range(1, meter_count + 1):
        meters_t = ["Elec-M%d" % meter_num,
                    "Electric_Meter_%d^Avg_Rate" % meter_num]
        for meter_t in meters_t:
            meter_groups[meter_t] = meter_num - 1
        devices.extend(meters_t)

    ts_list_t2, value_list_t2, device_data = get_ts_new_schema_electric(host, port, database,
                                                    username, password, source,
                                                    collection_name, building,
                                                    devices,
                                                    ['SIF_Electric_Demand',
                                                     'Electric_Utility'])
    ts_lists_t2, value_lists_t2 = [[], [], [], [], [], []], [[], [], [], [], [], []]
    for device, data in device_data.iteritems():
        print("device data len: %s:%s" % (len(data[0]), len(data[1])))
        group = meter_groups[device]
        print("device: %s, group: %s" % (device, group))
        ts_lists_t2   [group].extend(data[0])
        value_lists_t2[group].extend(data[1])

    print("ts_lists_t2: %s, %s" % (len(ts_lists_t2), len(ts_lists_t2[1])))
    print("value_lists_t2: %s, %s" % (len(value_lists_t2), len(value_lists_t2[1])))
    print(meter_groups)

    print("single-thread unified query took: %s" % misc.get_elapsed_tm(start_tm))
        # ts_lists_st.append(ts_list_t)
        # value_lists_st.append(value_list_t)

    df0 = _construct_electric_dataframe(ts_lists, value_lists).tz_localize(
                                                                       pytz.utc)
    df1 = _construct_electric_dataframe(ts_lists_st, value_lists_st).tz_localize(
                                                                       pytz.utc)
    df2 = _construct_electric_dataframe(ts_lists_t2, value_lists_t2).tz_localize(
        pytz.utc)
    return df2


def get_parsed_ts_new_schema(host, port, db_name, username, password,
                             source, collection_name, building, devices,
                             systems=None, floor=None, quad=None):
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
    :param devices: string or iterable
        device name(s) for identifying time series
    :param systems: string or iterable
        system name(s) for identifying time series
    :param floor: string
        floor identifier
    :param quad: string
        quadrant identifier

    :return: pandas DataFrame
        occupancy time series data
    """


    ts_list, val_list = get_ts_new_schema(host, port, db_name, username,
                                          password, source, collection_name,
                                          building, devices, systems,
                                          floor=floor, quad=quad)

    obs_df = pd.DataFrame({'obs': val_list}, index=ts_list).dropna()

    # drop missing values, set timestamp as the new index and sort by index
    # some duplicates seen in SIF steam data
    return obs_df.reset_index().drop_duplicates(subset='index').set_index(
        'index').sort_index().tz_localize(pytz.utc)['obs']


def _procees_doc(doc):

    readings = doc['readings']
    zipped = [(x['time'], x['value']) for x in readings
              if x['time'] is not None]

    if len(zipped):
        ts_list_t, val_list_t = zip(*zipped)
        return [ts_list_t, val_list_t]
    return [None, None]


def get_ts_new_schema(host, port, database, username, password, source,
                      collection_name, building, devices, systems=None,
                      floor=None, quad=None):
    """
    Get all observation data with the given building, devices and systems
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
    :param devices: string or iterable
        device name(s) for identifying time series
    :param systems: string or iterable
        system name(s) for identifying time series
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

        query = {"building": building}
        # there may be one or more devices to match
        if hasattr(devices, '__iter__'):
                 query['device'] = {'$in': devices}
        else:
            query['device'] = devices

       # systems is optional, for example for steam data
        # handle optional arguments
        for field, value in {'system': systems, 'floor': floor,
                             'quadrant': quad}.iteritems():
            if value:
                # there may be one or more systems names to match
                if hasattr(value, '__iter__'):
                    query[field] = {'$in': value}
                else:
                    query[field] = value

        # start_tm = datetime.datetime.utcnow()
        for data in collection.find(query):

            readings = data['readings']
            zipped = [(x['time'], x['value']) for x in readings
                                      if x['time'] is not None]

            if len(zipped):
                ts_list_t, val_list_t = zip(*zipped)
                ts_list.extend(ts_list_t)
                value_list.extend(val_list_t)

        # print("old post-process took: %s" % misc.get_elapsed_tm(start_tm))


        # start_tm = datetime.datetime.utcnow()
        # results = map(_procees_doc, collection.find(query))
        # [for ts_l, val_l in results if None not in [x,y]]
        # ts_list_new, value_list_new = zip(*results)
        # print("new post-process took: %s" % misc.get_elapsed_tm(start_tm))

    return ts_list, value_list


def get_ts_new_schema_electric(host, port, database, username, password, source,
                      collection_name, building, devices, systems=None,
                      floor=None, quad=None):
    """
    Get all observation data with the given building, devices and systems
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
    :param devices: string or iterable
        device name(s) for identifying time series
    :param systems: string or iterable
        system name(s) for identifying time series
    :param floor: string
        floor identifier
    :param quad: string
        quadrant identifier

    :return: tuple with a list of time stamps followed by a list of values
    """

    with pymongo.MongoClient(host, port) as conn:

        conn[database].authenticate(username, password, source=source)
        collection = conn[database][collection_name]

        ts_list, value_list, device_data = [], [], {}

        query = {"building": building}
        # there may be one or more devices to match
        if hasattr(devices, '__iter__'):
            query['device'] = {'$in': devices}
            for device in devices:
                device_data[device] = [[], []]
        else:
            query['device'] = devices
            device_data[devices] = [[], []]

        print(device_data)
        # handle optional arguments
        # systems is optional, for example for steam data
        for field, value in {'system': systems, 'floor': floor,
                             'quadrant': quad}.iteritems():
            if value:
                # there may be one or more systems names to match
                if hasattr(value, '__iter__'):
                    query[field] = {'$in': value}
                else:
                    query[field] = value

        # start_tm = datetime.datetime.utcnow()
        for doc in collection.find(query):

            device = doc['device']
            readings = doc['readings']
            zipped = [(x['time'], x['value']) for x in readings
                      if x['time'] is not None]

            if len(zipped):
                ts_list_t, val_list_t = zip(*zipped)
                ts_list.extend(ts_list_t)
                value_list.extend(val_list_t)

                device_str = str(device)
                device_data[device_str][0].extend(ts_list_t)
                device_data[device_str][1].extend(val_list_t)

                # print("old post-process took: %s" % misc.get_elapsed_tm(start_tm))


                # start_tm = datetime.datetime.utcnow()
                # results = map(_procees_doc, collection.find(query))
                # [for ts_l, val_l in results if None not in [x,y]]
                # ts_list_new, value_list_new = zip(*results)
                # print("new post-process took: %s" % misc.get_elapsed_tm(start_tm))

    return ts_list, value_list, device_data


