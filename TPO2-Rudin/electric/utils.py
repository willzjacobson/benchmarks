__author__ = 'ashishgagneja'

import pandas as pd
import common.utils


def _construct_dataframe(ts_lists, value_lists):

    # error checks
    if len(ts_lists) != len(value_lists):
        raise ValueError('array lengths must match')
    if not len(ts_lists):
        return None

    # ts_idx_t, value_list_t = _convert_datatypes(ts_lists[0], value_lists[0])
    # df = pd.Dataframe(data=value_list_t, index=ts_idx_t)

    # construct a superset of indices
    # super_index = pd.DatetimeIndex(ts_lists[0])
    # for ts_list in ts_lists[1:]:
    #     super_index = super_index.union(ts_list)

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
    print(total_df)

    # TODO: compute total demand
    print(master_df)
    return total_df



def _get_meter_data(meter_id, bldg_id, collection):

    ts_list, value_list = [], []
    for data in collection.find({"_id.building": bldg_id,
                                 "_id.device": "Elec-M%d" % meter_id,
                                 "_id.system": "SIF_Electric_Demand"}):

        readings = data['readings']
        zipped = map(lambda x: (x['time'], x['value']), readings)

        ts_list_t, value_list_t = zip(*zipped)
        ts_list.extend(ts_list_t)
        value_list.extend(value_list_t)

    return [ts_list, value_list]



def get_electric_ts(db, collection_name, bldg_id, meter_count, granularity):
    """ retrieves all available electric data from all meters and sums up
    to get total electric usage time series

    :param db: pymongo database object
        connected database object
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

    collection = db[collection_name]

    ts_lists, value_lists = [], []
    for equipment_id in range(1, meter_count+1):

        ts_list, value_list = _get_meter_data(equipment_id, bldg_id, collection)

        ts_lists.append(ts_list)
        value_lists.append(value_list)

    gran = "%dmin" % granularity
    return _construct_dataframe(ts_lists, value_lists)