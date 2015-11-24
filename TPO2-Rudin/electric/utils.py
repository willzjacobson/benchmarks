__author__ = 'ashishgagneja'

import pandas as pd
import common.utils
import joblib

def _construct_dataframe(ts_lists, value_lists):
    """
    Construct a pandas DataFrame using the time series data on individual
    meter can compute the total instantaneous usage

    :param ts_lists: list of lists
        list of
    :param value_lists:
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

        ts_idx_t, value_list_t = common.utils.convert_datatypes(ts_list,
                                                                value_lists[i])
        master_df = master_df.join(pd.DataFrame(data=value_list_t,
                                                index=ts_idx_t,
                                                columns=[str(i+1)]).dropna(),
                                   how='outer')

    total_df = master_df.sum(axis=1)
    print(type(total_df))
    return total_df.sort_index()


# TODO: this code can be generalized and used everywhere
# def _get_meter_data(meter_id, bldg_id, collection):
#
#     ts_list, value_list = [], []
#     for data in collection.find({"_id.building": bldg_id,
#                                  "_id.device": "Elec-M%d" % meter_id,
#                                  "_id.system": "SIF_Electric_Demand"}):
#
#         readings = data['readings']
#         zipped = map(lambda x: (x['time'], x['value']), readings)
#
#         ts_list_t, value_list_t = zip(*zipped)
#         ts_list.extend(ts_list_t)
#         value_list.extend(value_list_t)
#
#     return [ts_list, value_list]



def get_electric_ts(db_server, db_name, collection_name, bldg_id, meter_count,
                    granularity):
    """ retrieves all available electric data from all meters and sums up
    to get total electric usage time series

    :param db_server: string
        database server name or IP-address
    :param db_name: string
        name of the database on server
    :param collection_name: string
        database collection name to query
    :param bldg_id: string
        database building_id identifier
    :param meter_count: int
        number of distinct meters that need to be summed up
    :param granularity: int
        sampling frequency of input data and forecast data
    :return: pandas Dataframe
    """

    # collection = db[collection_name]

    ts_lists, value_lists = [], []
    # for equip_id in range(1, meter_count+1):

        # ts_list, value_list = _get_meter_data(equipment_id, bldg_id, collection)
        # ts_list, value_list = common.utils.get_ts(db_server, db_name,
        #                                            collection_name, bldg_id,
        #                                            "Elec-M%d" % equip_id,
        #                                            'SIF_Electric_Demand',
        #                                            'value')

        # ts_lists.append(ts_list)
        # value_lists.append(value_list)


    results = joblib.Parallel(n_jobs=-1, verbose=51)(joblib.delayed(
        common.utils.get_ts)(db_server, db_name, collection_name, bldg_id,
                             "Elec-M%d" % equip_id, 'SIF_Electric_Demand',
                             'value') for equip_id in range(1, meter_count+1))

    ts_lists, value_lists = zip(*results)

    # gran = "%dmin" % granularity
    return _construct_dataframe(ts_lists, value_lists)