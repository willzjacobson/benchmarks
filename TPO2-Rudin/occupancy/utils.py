__author__ = 'ashishgagneja'


import pandas as pd



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
                                'total')
    return pd.DataFrame(index=ts_list, data=val_list, columns=['occupancy'])


