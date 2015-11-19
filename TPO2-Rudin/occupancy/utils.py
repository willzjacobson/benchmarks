__author__ = 'ashishgagneja'

import pandas as pd
import dateutil.parser
import common.utils
import datetime


def _create_day_df(ts_list, val_list, col_label, drop_tz=True):


    # print(ts_list)
    # print(val_list)
    data = {'tstamp': ts_list, col_label: val_list}
    df_t = pd.DataFrame(data, columns=['tstamp', col_label])

    # drop rows with zeros
    df_t = df_t.loc[(df_t != 0).any(axis=1)]

    # convert timestamp string to datetime
    df_t[['tstamp']] = df_t['tstamp'].apply(
        lambda x: dateutil.parser.parse(x, ignoretz=drop_tz))

    return df_t.set_index('tstamp', verify_integrity=True).dropna().sort()



def _get_ts(collection, bldg_id, device, system, field, drop_tz=True):

    ts_list, value_list, daily_dict = [], [], {}

    for data in collection.find({"_id.building": bldg_id,
                                 "_id.device": device,
                                 "_id.system": system}):

        readings = data['readings']
        zipped = map(lambda x: (x['time'], x[field]), readings)

        ts_list_t, val_list_t = zip(*zipped)
        # ts_list_t, val_list_t = common.utils.convert_datatypes(ts_list_t,
        #                                                    val_list_t,
        #                                                    val_type=None)

        # save day's data
        # data_dt = dateutil.parser.parse(data['_id']['date'],
        #                                 ignoretz=drop_tz).date()
        # daily_dict[data_dt] = _create_day_df(ts_list_t, val_list_t, 'occupancy')

        ts_list.extend(ts_list_t)
        value_list.extend(val_list_t)
        # ts_list.extend(list(daily_dict[data_dt].index))
        # value_list.extend(daily_dict[data_dt]['occupancy'].tolist())

    return ts_list, value_list



def get_occupancy_ts(db, collection_name, bldg_id):
    collection = db[collection_name]

    ts_list, val_list = _get_ts(collection, bldg_id, 'Occupancy',
                                              'Occupancy', 'value')
    # print(ts_list[1:100])

    ts_list, val_list = common.utils.convert_datatypes(ts_list, val_list,
                                                       val_type=None)
    df = pd.DataFrame(index=ts_list, data=val_list,
                      columns=['occupancy'])
    return df.dropna().sort()


