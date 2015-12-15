# coding=utf-8
__author__ = 'ashishgagneja'

import joblib
import pandas as pd

import common.utils


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
        ts_idx_t, value_list_t = common.utils.convert_datatypes(ts_list,
                                                                value_lists[i])
        # create new column
        master_df = master_df.join(pd.DataFrame(data=value_list_t,
                                                index=ts_idx_t,
                                                columns=[str(i+1)]).dropna(),
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

        # ts_list, value_list = _get_meter_data(equipment_id, bldg_id, collection)
    # ts_list, value_list = common.utils.get_ts(host, database,
        #                                            collection_name, bldg_id,
        #                                            "Elec-M%d" % equip_id,
        #                                            'SIF_Electric_Demand',
        #                                            'value')

        # ts_lists.append(ts_list)
        # value_lists.append(value_list)


    results = joblib.Parallel(n_jobs=-1)(joblib.delayed(common.utils.get_ts)(
        host, port, database, username, password, source_db, collection_name,
        bldg_id, "Elec-M%d" % equip_id, 'SIF_Electric_Demand', 'value')
            for equip_id in range(1, meter_count+1))

    ts_lists, value_lists = zip(*results)

    # gran = "%dmin" % granularity
    return _construct_dataframe(ts_lists, value_lists)