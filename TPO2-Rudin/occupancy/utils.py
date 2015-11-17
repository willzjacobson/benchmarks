__author__ = 'ashishgagneja'


import pandas as pd
import common.utils


def _get_ts(collection, bldg_id, device, system, field):

    ts_list, value_list = [], []
    for data in collection.find({"_id.building": bldg_id,
                                 "_id.device": device,
                                 "_id.system": system}):

        readings = data['readings']
        zipped = map(lambda x: (x['time'], x[field]), readings)

        ts_list_t, value_list_t = zip(*zipped)
        ts_list.extend(ts_list_t)
        value_list.extend(value_list_t)

    return [ts_list, value_list]



def get_occupancy_ts(db, collection_name, bldg_id):
    collection = db[collection_name]

    ts_list, val_list = _get_ts(collection, bldg_id, 'Occupancy', 'Occupancy',
                                'value')
    print(ts_list[1:100])
    ts_list, val_list = common.utils.convert_datatypes(ts_list, val_list,
                                                       val_type=None)
    df = pd.DataFrame(index=ts_list, data=val_list,
                      columns=['occupancy'])
    return df.dropna().sort()


