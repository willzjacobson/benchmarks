__author__ = 'ashishgagneja'

import pandas as pd
import common.utils
import dateutil.parser
import numpy

def _get_ts(collection, bldg_id, device, system, field, drop_tz=True):

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



def get_occupancy_ts(db, collection_name, bldg_id):
    collection = db[collection_name]

    ts_list, val_list = _get_ts(collection, bldg_id, 'Occupancy',
                                              'Occupancy', 'value')
    # ts_list, val_list = common.utils.convert_datatypes(ts_list, val_list,
    #                                                    val_type=None)
    occ_df = pd.DataFrame({'tstamp': ts_list, 'occupancy': val_list})
    occ_df['tstamp'] = occ_df['tstamp'].apply(
        lambda x: dateutil.parser.parse(x, ignoretz=True)
        if type(x) is not int else numpy.nan)

    occ_df = occ_df.dropna().set_index('tstamp', verify_integrity=True).sort()
    return occ_df


