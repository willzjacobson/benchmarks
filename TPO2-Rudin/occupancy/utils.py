__author__ = 'ashishgagneja'

import pandas as pd
import common.utils
import datetime
import sys


# TODO: this code can be generalized and used everywhere
# def _get_ts(collection, bldg_id, device, system, field):
#
#     ts_list, value_list, daily_dict = [], [], {}
#
#     for data in collection.find({"_id.building": bldg_id,
#                                  "_id.device": device,
#                                  "_id.system": system}):
#
#         readings = data['readings']
#         zipped = map(lambda x: (x['time'], x[field]), readings)
#
#         ts_list_t, val_list_t = zip(*zipped)
#
#         ts_list.extend(ts_list_t)
#         value_list.extend(val_list_t)
#
#     return ts_list, value_list



def get_occupancy_ts(db_server, db_name, collection_name, bldg_id, drop_tz=True):
    """Fetch all available occupancy data from database

    :param db_server: string
        database server name or IP-address
    :param db_name: string
        name of the database on server
    :param collection_name: string
        collection name to use
    :param bldg_id: string
        building identifier

    :return: pandas DataFrame
        occupancy time series data
    """

    ts_list, val_list = common.utils.get_ts(db_server, db_name, collection_name,
                                            bldg_id, 'Occupancy', 'Occupancy',
                                            'value')

    # parse timestamp and observation to appropriate datatypes
    ts_list, val_list = common.utils.convert_datatypes(ts_list, val_list,
                            drop_tz=drop_tz, val_type=None)

    # it is not possible to create a pandas Series object directly as
    # placeholder entries may be there for missing data. these are usually
    # in the form of time:0 associated with value:0
    occ_df = pd.DataFrame({'tstamp': ts_list, 'occupancy': val_list})
    # occ_df['tstamp'] = occ_df['tstamp'].apply(
    #     lambda x: dateutil.parser.parse(x, ignoretz=drop_tz)
    #     if type(x) is not int else numpy.nan)

    # drop missing values, set timestamp as the new index and sort by index
    return occ_df.dropna().set_index('tstamp',
                                     verify_integrity=True).sort_index()



def score_occ_similarity(base_dt, date_shortlist, occ_ts):

    # TODO: when we have occupancy forecast, use that to obtain expected
    # occupancy. For now, use actual
    base_ts = common.utils.get_dt_tseries(base_dt, occ_ts)
    base_ts_nodate = common.utils.drop_series_ix_date(base_ts)
    # print(bench_dt_occ_fcst)

    one_day = datetime.timedelta(days=1)
    scores = []
    for dt_t in date_shortlist:

        end_idx = datetime.datetime.combine(dt_t + one_day, datetime.time.min)
        score = common.utils.compute_profile_similarity_score(base_ts_nodate,
                    common.utils.drop_series_ix_date(occ_ts[dt_t: end_idx]))
        scores.append((dt_t, score))

    return scores.sort(key=lambda x: x if x else sys.maxint)