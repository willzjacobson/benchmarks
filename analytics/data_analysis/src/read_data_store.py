__author__ = 'ashishgagneja'

import pandas as pd

HDF5_file = '/data/park345_1a_1b.h5'

store_iter = pandas.read_hdf(HDF5_file, 'df', iterator=True)

for ts in sore_iter:
    print ts