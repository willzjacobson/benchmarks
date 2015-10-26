__author__ = 'ashishgagneja'

import pandas as pd
import pickle
import os
import json

HDF5_file = '/data/park345_1a_1b.h5'
GROUPS_PICKLE_file = '/home/ashishgagneja/misc/groups.pickle'

groups = None

# if not os.path.exists(GROUPS_PICKLE_file):
#

#print('pickle file not found\n')
store = pd.HDFStore(HDF5_file)

# find distinct timeseries
df = store.select('df')
grouped = df.groupby(['Controller', 'Subcontroller', 'PointName'], sort=False)
groups = grouped.groups

with open('/home/ashishgagneja/misc/groups.json', 'wb+') as f:
    json.dump(groups, f)

store.close()

#
# else:
#     print('loading pickle\n')
#     with open(GROUPS_PICKLE_file, 'rb') as f:
#         groups = pickle.load(f)
#)


# write group keys
for k, v in groups.iteritems():
    ctrlr, sub_cntrlr, pt_nm = k
    print('%s,%s,%s' % (ctrlr, sub_cntrlr, pt_nm))


