# coding: utf-8
# from IPython.parallel import Client
# rc=Client()
import pandas as pd

from custom_fncs import misc

# for wide terminal display of pandas dataframes
# pd.options.display.width = 120
# pd.options.display.max_rows = 10000
# from IPython import get_ipython

# plot inline
# get_ipython().magic('pylab inline')
# IPython.get_ipython().magic('matplotlib inline')

# plt.rcParams['figure.figsize'] = 14, 6

directory = '~/Documents/workspace/data_analysis/'
csv_file = 'data/park345_CHLR1.csv'
title = 'Accumulated Steam Usage'

# load dataframe, and subset out relevant columns
park_data = pd.read_csv(directory + csv_file, error_bad_lines=False)
park_data.columns = ['ID', 'TIMESTAMP',
                     'TRENDFLAGS', 'STATUS',
                     'VALUE', 'TRENDFLAGS_TAG',
                     'STATUS_TAG']
park_data = park_data.sort('TIMESTAMP')

# TODO Note that lags necessary for season stationarity>100 w-out log transform
# is over 100 for non-log-ratio transformed original data, and 0
# for log-ratio transformed

# construct time series, getting rid of microseconds
park_ts = pd.Series(list(park_data.VALUE),
                    pd.DatetimeIndex(park_data.TIMESTAMP),
                    name=title)

park_ts.drop_duplicates(inplace=True)
park_ts = park_ts.loc[park_ts != 0].resample('15Min').interpolate()

misc.start_time(park_ts)

# park_ts_logr = (park_ts / park_ts.shift(1)).apply(sp.log)[1:]
