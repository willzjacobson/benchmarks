__author__ = 'ashishgagneja'

import pandas as pd
import pickle
import os
import json
import itertools
import numpy as np


HDF5_file = '/data/park345_1a_1b.h5'
GROUPS_PICKLE_file = '/home/ashishgagneja/misc/groups.pickle'

groups = None

# if not os.path.exists(GROUPS_PICKLE_file):
#

#print('pickle file not found\n')
store = pd.HDFStore(HDF5_file)

# find distinct timeseries
df = store.select('df')
#grouped = df.groupby(['Controller', 'Subcontroller', 'PointName'], sort=False)
#groups = grouped.groups

controller_list = pd.unique(df['Controller'].ravel())
controller_list = np.delete(controller_list, np.nan)

subcontroller_list = pd.unique(df['Subcontroller'].ravel())
subcontroller_list = np.delete(subcontroller_list, np.nan)

pointname_list = pd.unique(df['PointName'].ravel())
pointname_list = np.delete(pointname_list, np.nan)

cross_product = itertools.product(controller_list, subcontroller_list, pointname_list)

valid_keys = {}
for key in cross_product:
    ctrlr, sub_cntrlr, pt_nm = key
    tmp_dt = df[(df.Controller == ctrlr) & (df.Subcontroller == sub_cntrlr) & (df.PointName == pt_nm)]
    if tmp_dt.size:
        valid_keys[key] = tmp_dt.size


with open('/home/ashishgagneja/misc/valid_keys.json', 'wb+') as f:
    json.dump(valid_keys, f)

store.close()

#
# else:
#     print('loading pickle\n')
#     with open(GROUPS_PICKLE_file, 'rb') as f:
#         groups = pickle.load(f)
#)

# write group keys
#for k, v in groups.iteritems():
#    ctrlr, sub_cntrlr, pt_nm = k
#    print('%s,%s,%s' % (ctrlr, sub_cntrlr, pt_nm))


