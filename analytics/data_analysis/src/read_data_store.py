__author__ = 'ashishgagneja'

import pandas as pd

HDF5_file = '/data/park345_1a_1b.h5'

store = pd.HDFStore(HDF5_file)

# find distinct timeseries
df = store.select('df')
grouped = df.groupby(['Controller', 'Subcontroller', 'PointName'])
groups = grouped.groups()

# write group keys
for k, v in groups.iteritems():
    ctrlr, sub_cntrlr, pt_nm = k
    print('%s,%s,%s' % (ctrlr, subcntrlr, pt_nm))

store.close()

