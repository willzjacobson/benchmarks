# coding: utf-8
# from IPython.parallel import Client
# rc=Client()
import pandas as pd
# for wide terminal display of pandas dataframes
pd.options.display.width = 120
#pd.options.display.max_rows = 10000
# from IPython import get_ipython
import statsmodels.graphics.tsaplots as tsp
from custom_fncs.misc import *

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

park_ts_logr = (park_ts / park_ts.shift(1)).apply(sp.log)[1:]

# d = _number_diff(park_ts)
# p = _number_ar_terms(park_ts)

park_ts.plot()
tsp.plot_acf(park_ts['06-04-2013'])
tsp.plot_pacf(park_ts['06-04-2013'])
tsp.plot_acf(park_ts_logr['06-04-2013'])
tsp.plot_pacf(park_ts_logr['06-04-2013'])
number_diff(park_ts_logr['06-04-2013'])
number_diff(park_ts['06-04-2013'])
'''
From this data, an ARIMA(1,1,1) seems reasonable. We remark, however,
that taking the log-ratios has resulted in our needing more differencing
at 06-04-2013 to induce stationarity.
'''
tsp.plot_acf(park_ts.at_time('10:30:00'))
tsp.plot_pacf(park_ts.at_time('10:30:00'))
tsp.plot_acf(park_ts_logr.at_time('10:30:00'))
tsp.plot_pacf(park_ts_logr.at_time('10:30:00'))
number_diff(park_ts_logr.at_time('10:30:00'))
number_diff(park_ts.at_time('10:30:00'))
'''
If modeling individual times for the log ratio time series,
the PACF and ACF clearly indicate seasonal $(P,D,Q) = (1,1,0)$,
while for the log-ratio time series, we obtain seasonal
$(0,0,0)$. By becoming too granular, we have
reduced our seasonal data subset to white noise.
'''

tsp.plot_acf(park_ts_logr['06-04-2013'])
tsp.plot_pacf(park_ts_logr['06-04-2013'])

tsp.plot_acf(park_ts_logr.at_time('10:30:00'))
tsp.plot_pacf(park_ts_logr.at_time('10:30:00'))

number_diff(park_ts_logr['06-01-2013':'07-01-2013'])
#
# actual_vs_prediction(park_ts)
number_diff(park_ts['06-01-2013':'07-01-2013'])
actual_vs_prediction(park_ts['06-01-2013':'07-01-2013'])
actual_vs_prediction(park_ts['06-01-2013':'08-08-2013'], days=(0, 1, 2),
                     order=(1, 1, 0), seasonal_order=(1, 1, 0, 96))



# for testing
# actual_vs_prediction(park_ts['06-01-2013':'08-08-2013'], days=(0,1,2,3,4,5,6),
#                      order=(1, 1, 0), seasonal_order=(1, 1, 0, 96))

# actual_vs_prediction(park_ts['06-01-2013':'08-08-2013'], days=(0,1,2),
#                      order=(1, 1, 0), seasonal_order=(1, 1, 0, 96))

mod1 = sarimax.SARIMAX(park_ts['2013-06-01':'2013-07-08'], order=(1, 0, 0),
                       seasonal_order=(0, 1, 0, 96))
