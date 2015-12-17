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


def _construct_dataframe(ts_lists, value_lists):
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
                    collection_name, bldg_id, meter_count):
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
    :param bldg_id: string
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
            bldg_id, "Elec-M%d" % equip_id, 'SIF_Electric_Demand', 'value')
                                         for equip_id in
                                         range(1, meter_count + 1))

    ts_lists, value_lists = zip(*results)

    # gran = "%dmin" % granularity
    return _construct_dataframe(ts_lists, value_lists)


def get_occupancy_ts(host, port, database, username, password, source_db,
                     collection_name, bldg_id, drop_tz=True):
    """Fetch all available occupancy data from database

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
        collection name to use
    :param bldg_id: string
        building identifier
    :param drop_tz: bool
        whether to drop timezone information

    :return: pandas DataFrame
        occupancy time series data
    """

    ts_list, val_list = get_ts(host, port, database, username, password,
                               source_db, collection_name, bldg_id, 'Occupancy',
                               'Occupancy', 'value')

    # parse timestamp and observation to appropriate datatypes
    ts_list, val_list = ts_proc.munge.convert_datatypes(ts_list, val_list,
                                                        drop_tz=drop_tz,
                                                        val_type=None)

    # it is not possible to create a pandas Series object directly as
    # placeholder entries may be there for missing data. these are usually
    # in the form of time:0 associated with value:0
    occ_df = pd.DataFrame({'tstamp': ts_list, 'occupancy': val_list})

    # drop missing values, set timestamp as the new index and sort by index
    occ_df = occ_df.dropna().set_index('tstamp',
                                       verify_integrity=True).sort_index()
    return occ_df['occupancy']


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
    collection = db[collection_name]
    for data in collection.find({"_id.building": bldg,
                                 "_id.device": "Space_Temp",
                                 "_id.floor": str(floor),
                                 "_id.quad": quad}):
        readings = data['readings']
        for reading in readings:
            ts_list.append(
                    dateutil.parser.parse(reading['time'], ignoretz=True))
            value_list.append(float(reading['value']))

    gran = "%dmin" % granularity
    return pd.Series(data=value_list, index=pd.DatetimeIndex(ts_list)
                     ).sort_index().resample(gran)


def get_ts(host, port, database, username, password, source_db,
           collection_name, bldg_id, device, system, field):
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
    :param source_db: string
        source database for authentication
    :param collection_name: string
        database collection name
    :param bldg_id: string
        building identifier
    :param device: string
        device name for identifying time series
    :param system: string
        system name for identifying time series
    :param field: string
        field name for identifying time series

    :return: tuple with a list of time stamps followed by a list of values
    """

    with pymongo.MongoClient(host, port) as conn:
        conn[database].authenticate(username, password, source=source_db)
        collection = conn[database][collection_name]

        ts_list, value_list, daily_dict = [], [], {}
        for data in collection.find({"_id.building": bldg_id,
                                     "_id.device": device,
                                     "_id.system": system}):
            readings = data['readings']
            zipped = map(lambda x: (x['time'], x[field]), readings)

            ts_list_t, val_list_t = zip(*zipped)

            ts_list.extend(ts_list_t)
            value_list.extend(val_list_t)

    return ts_list, value_list
