__author__ = 'ashishgagneja'

import pandas as pd
import dateutil



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

        ts_idx_t, value_list_t = _convert_datatypes(ts_list, value_lists[i])
        print('%s:%s' % (type(ts_idx_t), type(value_list_t)))
        # df = pd.DataFrame(data=value_list_t, index=ts_idx_t,
        #                   columns=["%d" % i+1])
        master_df += pd.DataFrame(data=value_list_t, index=ts_idx_t,
                                  columns=[str(i+1)])

    print(master_df)
    return master_df



def _convert_datatypes(ts_list, value_list, drop_tz=True):

    ts_list = list(map(lambda x: dateutil.parser.parse(reading['time'],
                                                    ignoretz=drop_tz), ts_list))
    print(ts_list)

    # convert str to float
    value_list = list(map(float, value_list))

    return [ts_list, value_list]




def get_electric_ts(db, collection_name, bldg_id, meter_count, granularity):
    """ retrieves all available electric data from all meters and sums up
    to get total electric usage time series

    :param db: pymongo database object
        connected database object
    :param collection_name: string
        database collection name to query
    :param bldg_id: string
        database building identifier
    :param meter_count: int
        number of distinct meters that need to be summed up
    :param granularity: int

    :return: pandas Dataframe
    """

    collection = db[collection_name]

    ts_lists, value_lists = [], []
    for equipment_id in range(1, meter_count+1):

        ts_list, value_list = [], []
        for data in collection.find({"_id.building": bldg_id,
                                     "_id.device": "Elec-M%d" % equipment_id,
                                     "_id.system": "SIF_Electric_Demand"}):

            readings = data['readings']
            # print(readings)
            try:
                zipped = map(lambda x: (x['time'], x['value']), readings)
            except Exception as e:
                print('Failure <%s> on %s' % (e, readings))
                continue

            # ts_list.extend(map(lambda x: x['time']), readings)
            # value_list.extend(map(lambda x: x['value']), readings)
            ts_list_t, value_list_t = zip(*zipped)
            ts_list.extend(ts_list_t)
            value_list.extend(value_list_t)

            # for reading in readings:
            #     ts_list.append(
            #         dateutil.parser.parse(reading['time'], ignoretz=True))
            #     value_list.append(float(reading['value']))

        ts_lists.append(ts_list)
        value_lists.append(value_list)

    # remove tz information
    # ts_list = map(lambda x: dateutil.parser.parse(reading['time'],
    #                                               ignoretz=True), ts_list)
    # convert str to float
    # value_list = map(float, value_list)

    df = _construct_dataframe(ts_lists, value_lists)
    gran = "%dmin" % granularity
    # return pd.Series(data=value_list, index=pd.DatetimeIndex(ts_list)
    #                  ).sort_index().resample(gran)
    return df