# coding=utf-8
# import IPython.parallel

# rc = IPython.parallel.Client()
# dview = rc[:]
# dview.block = True

# with dview.sync_imports():
import dateutil.parser
import pymongo

# from statsmodels.tsa.statespace.sarimax import SARIMAX
# import seaborn as sns
import pandas as pd
import joblib
# sns.set()
import ts_proc.munge
import dateutil.parser


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

    # error checks
    if len(ts_lists) != len(value_lists):
        raise ValueError('array lengths must match')
    if not len(ts_lists):
        return None

    master_df = pd.DataFrame()
    # insert column data
    for i, ts_list in enumerate(ts_lists):
        # convert column data and index to appropriate type
        ts_idx_t, value_list_t = ts_proc.munge.convert_datatypes(ts_list,
                                                                 value_lists[i])
        # create new column
        master_df = master_df.join(pd.DataFrame(data=value_list_t,
                                                index=ts_idx_t,
                                                columns=[str(i + 1)]).dropna(),
                                   how='outer')

    return master_df.sum(axis=1).sort_index()


def get_electric_ts(host, port, database, username, password, source_db,
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
    :param source_db: string
        source database for authentication
    :param collection_name: string
        database collection name to query
    :param building: string
        database building_id identifier
    :param meter_count: int
        number of distinct meters that need to be summed up

    :return: pandas Dataframe
    """

    # ts_lists, value_lists = [], []
    # for equip_id in range(1, meter_count+1):

    # ts_list, value_list = _get_meter_data(
    # equipment_id, bldg_id, collection)
    # ts_list, value_list = common.utils.get_ts(host, database,
    #                                            collection_name, bldg_id,
    #                                            "Elec-M%d" % equip_id,
    #                                            'SIF_Electric_Demand',
    #                                            'value')

    # ts_lists.append(ts_list)
    # value_lists.append(value_list)


    results = joblib.Parallel(n_jobs=-1)(joblib.delayed(get_ts)(
            host, port, database, username, password, source_db,
            collection_name,
            building, "Elec-M%d" % equip_id, 'SIF_Electric_Demand', 'value')
                                         for equip_id in
                                         range(1, meter_count + 1))

    ts_lists, value_lists = zip(*results)

    # gran = "%dmin" % granularity
    return _construct_electric_dataframe(ts_lists, value_lists)


def get_occupancy_ts(host, port, source, username, password, db_name,
                     collection_name, building):
    """Fetch all available occupancy data from database

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
    :return: pandas DataFrame
        occupancy time series data
    """

    ts_list, val_list = get_ts(host, port, db_name, username, password,
                               source, collection_name, building, 'Occupancy',
                               'Occupancy')

    # parse timestamp and observation to appropriate datatypes
    ts_list, val_list = ts_proc.munge.convert_datatypes(ts_list, val_list,
                                                        val_type=None)

    # it is not possible to create a pandas Series object directly as
    # placeholder entries may be there for missing data. these are usually
    # in the form of time:0 associated with value:0
    occ_df = pd.DataFrame({'tstamp': ts_list, 'occupancy': val_list})

    # drop missing values, set timestamp as the new index and sort by index
    occ_df = occ_df.dropna().set_index('tstamp',
                                       verify_integrity=True).sort_index()
    return occ_df.loc['occupancy']


def get_space_temp_ts(db, collection_name, bldg, floor, quad, granularity):
    """ retrieve all available space temperature data for floor-quad of
        building_id bldg

    :param db: pymongo database object
        connected database object
    :param collection_name: string
        database collection name
    :param bldg: string
        database building_id identifier
    :param floor: string
        floor identifier
    :param quad: string
        quadrant identifier
    :param granularity: int
    sampling frequency of input data and forecast data

    :return: pandas Series
    """

    ts_list, value_list = [], []
    collection = db.loc[collection_name]
    for data in collection.find({"_id.building": bldg,
                                 "_id.device": "Space_Temp",
                                 "_id.floor": str(floor),
                                 "_id.quad": quad}):
        readings = data.loc['readings']
        for reading in readings:
            ts_list.append(
                    dateutil.parser.parse(reading['time'], ignoretz=True))
            value_list.append(float(reading['value']))

    return pd.Series(data=value_list, index=pd.DatetimeIndex(ts_list)
                     ).sort_index()


def get_parsed_ts(host, port, database, username, password, source,
                  collection_name, building, device, system):
    """Fetch all available timeseries data from database

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
        collection name to use
    :param building: string
        building identifier
    :param device: string
        device name for identifying time series
    :param system: string
        system name for identifying time series
    :return: pandas DataFrame
        occupancy time series data
    """

    ts_list, val_list = get_ts(host, port, database, username, password,
                               source, collection_name, building, device,
                               system)

    # parse timestamp and observation to appropriate datatypes
    # this is no longer needed
    # ts_list, val_list = ts_proc.munge.convert_datatypes(ts_list, val_list,
    #                                                     val_type=val_type)

    # it is not possible to create a pandas Series object directly as
    # placeholder entries may be there for missing data. these are usually
    # in the form of time:0 associated with value:0
    obs_df = pd.DataFrame({'tstamp': ts_list, 'obs': val_list})

    # drop missing values, set tstamp as the new index and sort by index
    return obs_df.dropna().set_index(
        'tstamp').drop_duplicates().sort_index()['obs']
    # 'tstamp', verify_integrity=True).sort_index()['obs']


def get_ts(host, port, database, username, password, source, collection_name,
           building, device, system):
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
    :return: tuple with a list of time stamps followed by a list of values
    """

    with pymongo.MongoClient(host, port) as conn:
        conn[database].authenticate(username, password, source=source)
        collection = conn[database][collection_name]

        ts_list, value_list, daily_dict = [], [], {}
        for data in collection.find({"_id.building": building,
                                     "_id.device": device,
                                     "_id.system": system}):
            readings = data['readings']

            # zipped = map(lambda x: (x.loc['time'], x.loc["value"]), readings)
            # print(readings)
            # sys.exit(0)
            zipped = [(x['time'], x['value']) for x in readings
                      if (x['time'] is not None
                          and type(x['time']) is not int
                          and 'value' in x)]

            if len(zipped):
                ts_list_t, val_list_t = zip(*zipped)

                ts_list.extend(ts_list_t)
                value_list.extend(val_list_t)

    return ts_list, value_list



def get_parsed_ts_new_schema(host, port, database, username, password,
                             source, collection_name, building, device,
                             system):
    """Fetch all available timeseries data from database

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
        collection name to use
    :param building: string
        building identifier
    :param device: string
        device name for identifying time series
    :param system: string
        system name for identifying time series

    :return: pandas DataFrame
        occupancy time series data
    """

    ts_list, val_list = get_ts_new_schema(host, port, database, username,
                                          password, source, collection_name,
                                          building, device, system)

    # parse timestamp and observation to appropriate datatypes
    # 2016-01-05: the old schema has been changed to have timestamps as
    # ISOTime objects so parsing timestamps is no longer needed
    # ts_list, val_list = ts_proc.munge.convert_dtypes_new_schema(ts_list,
    #                             val_list, val_type=val_type)

    # it is not possible to create a pandas Series object directly as
    # placeholder entries may be there for missing data. these are usually
    # in the form of time:0 associated with value:0 and/or NAs
    obs_df = pd.DataFrame({'tstamp': ts_list, 'obs': val_list})

    # drop missing values, set timestamp as the new index and sort by index
    # some duplicates seen in SIF steam data
    return obs_df.dropna().set_index('tstamp').sort_index()['obs']



def get_ts_new_schema(host, port, database, username, password, source,
                      collection_name, building, device, system):
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
    # :param field: string
    #     field name for identifying time series

    :return: tuple with a list of time stamps followed by a list of values
    """

    with pymongo.MongoClient(host, port) as conn:

        conn[database].authenticate(username, password, source=source)
        collection = conn[database][collection_name]

        ts_list, value_list, daily_dict = [], [], {}
        for data in collection.find({"building": building,
                                     "device": device,
                                     "system": system}):

            readings = data['readings']

            # zipped = map(lambda x: (x['time'], x['value']) if
            # 'value' in x, readings)
            # some occupancy data has reading entries with just the timestamp
            # and no "value" key
            # zipped = [(x['time'], x['value']) for x in readings if 'value' in x]
            zipped = [(x['time'], x['value']) for x in readings
                                                if x['time'] is not None]

            if len(zipped):
                ts_list_t, val_list_t = zip(*zipped)
                ts_list.extend(ts_list_t)
                value_list.extend(val_list_t)

    return ts_list, value_list


