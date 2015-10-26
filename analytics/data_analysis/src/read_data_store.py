__author__ = 'ashishgagneja'

import pandas as pd
import pickle
import os


HDF5_file = '/data/park345_1a_1b.h5'
GROUPS_PICKLE_file = '/home/ashishgagneja/misc/groups.pickle'

groups = None

if not os.path.isfile(GROUPS_PICKLE_file):

    store = pd.HDFStore(HDF5_file)

    # find distinct timeseries
    df = store.select('df')
    grouped = df.groupby(['Controller', 'Subcontroller', 'PointName'], sort=False)
    groups = grouped.groups

    store.close()

else:
    with open(GROUPS_PICKLE_file, 'rb') as f:
        groups = pickle.load(f)


# write group keys
for k, v in groups.iteritems():
    ctrlr, sub_cntrlr, pt_nm = k
    print('%s,%s,%s' % (ctrlr, subcntrlr, pt_nm))


