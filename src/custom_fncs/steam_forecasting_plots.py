# coding: utf-8

import pandas as pd
# for wide terminal display of pandas dataframes
pd.options.display.width = 120
pd.options.display.max_rows = 10000
import numpy as np
import statsmodels.tsa.arima_model as arima
# from IPython import get_ipython

# plot inline
# get_ipython().magic('pylab inline')
# IPython.get_ipython().magic('matplotlib inline')
import matplotlib.pylab as pylab

pylab.rcParams['figure.figsize'] = 14, 6

directory = '/Users/davidkarapetyan/Documents/workspace/data_analysis/'
csv_file = 'data/park345_steam.csv'


# load dataframe, and subset out relevant columns
park_data = pd.read_csv(directory + csv_file, error_bad_lines=False)
park_data.columns = ['ID', 'TIMESTAMP',
                     'TRENDFLAGS', 'STATUS',
                     'VALUE', 'TRENDFLAGS_TAG',
                     'STATUS_TAG']
park_data = park_data.sort('TIMESTAMP')


# construct time series, getting rid of microseconds
park_ts = pd.Series(list(park_data.VALUE),
                    pd.DatetimeIndex(park_data.TIMESTAMP),
                    name="steam values")

park_ts = park_ts.loc[park_ts != 0].resample('15Min ').interpolate()
print(park_ts)

park_ts_filter = park_ts[
    np.logical_and(park_ts.index.weekday == 0, park_ts < park_ts.shift(1))]
print(park_ts_filter)

'''
Observe that almost all the data is for 15 minutes after midnight.
Hence, it is reasonable to exclude all other times from our analysis,
and to fill in gaps via interpolation.
'''

park_ts_filter_15 = park_ts_filter[
    park_ts_filter.index.minute == 15].interpolate()

basic_stats_15 = park_ts_filter_15.describe(percentiles=[0.05, 0.95])
print(arima.ARIMA(park_ts_filter_15[park_ts_filter_15.between(
    basic_stats_15['5%'],
    basic_stats_15['95%'])], order=(0, 1, 0)).fit().summary())

'''
This suggests that the spikes in our data are indeed very random, and are
not easily modeled via a white noise parameter (and so, there may be a more
appropriate model than ARIMA). For now, we use ARIMA to forecast these values,
and compare them with the actual values.
'''

# park_ts_filter_15 = park_ts_filter_15[park_ts_filter_15.between(
#     basic_stats_filter_15['mean'] - 2 * basic_stats_filter_15['5%'],
#     basic_stats_filter_15['mean'] + basic_stats_filter_15['95%'])]
# park_ts_filter_15 = park_ts_filter_15.resample('7D').interpolate()

# fit_ar_100 = arima.ARIMA(park_ts_filter_15, order=(1, 0, 0)).fit()

'''
The fit is still not very good.
'''

# TODO Get feedback from Gene about why this is occurring.
# Believe it to be a BMS error.
