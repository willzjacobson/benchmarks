# coding: utf-8
import pandas as pd

import config
import arima.model
import common.utils


cfg = config.ashish

# for wide terminal display of pandas dataframes
# pd.options.display.width = 120
# pd.options.display.max_rows = 10000
# from IPython import get_ipython

# plot inline
# get_ipython().magic('pylab inline')
# IPython.get_ipython().magic('matplotlib inline')

# plt.rcParams['figure.figsize'] = 14, 6

# directory = '/home/davidkarapetyan/Documents/workspace/data_analysis/'
# csv_file = 'data/oa_temp.csv'
title = 'Accumulated Steam Usage'
park_data = pd.read_hdf(cfg['345_Park']['steam_data'],
                        cfg['345_Park']['steam_data_group'])

# TODO Note that lags necessary for season stationarity>100 w-out log transform
# is over 100 for non-log-ratio transformed original data, and 0
# for log-ratio transformed

# construct time series, getting rid of microseconds
park_ts = pd.Series(list(park_data.VALUE),
                    pd.DatetimeIndex(park_data.TIMESTAMP),
                    name=title)

# bottom creates massive data errors; bms must output
# flag for when values are the same, but valid
# park_ts.drop_duplicates(inplace=True)
# park_ts = park_ts.loc[park_ts != 0].resample('15Min').interpolate()

granularity = cfg['sampling']['granularity']
park_ts = common.utils.interp_tseries(park_ts.resample('%dMin' % granularity),
                                      granularity)

prediction = arima.model.start_time(park_ts,
                                    cfg['weather']['h5file'],
                                    cfg['weather']['history'],
                                    cfg['weather']['forecast'],
                                    cfg['arima']['order'],
                                    granularity)
print(prediction)
