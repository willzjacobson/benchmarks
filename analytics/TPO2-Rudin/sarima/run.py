# coding: utf-8
# from IPython.parallel import Client
# rc=Client()
import pandas as pd
import weather
import json
import os
import config

# load configuration
# config = None
# with open('/home/ashishgagneja/Adirondack/analytics/TPO2-Rudin/config.py') as f:
#     config = json.load(f)
#
# if config is None:
#     raise Exception('configuration load failed')

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
# title = 'Accumulated Steam Usage'

# load dataframe, and subset out relevant columns
# park_data = pd.read_csv(directory + csv_file, error_bad_lines=False)
# park_data.columns = ['ID', 'TIMESTAMP',
#                      'TRENDFLAGS', 'STATUS',
#                      'VALUE', 'TRENDFLAGS_TAG',
#                      'STATUS_TAG']
# park_data = park_data.sort('TIMESTAMP')
park_data = pd.read_hdf(cfg.park345.steam_data, cfg.park345.steam_data_group)

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

park_ts = park_ts.resample('15Min')
# park_ts = park_ts['2013-04-01': '2013-07-01']
# start_up._benchmark_ts(park_ts, datetime="2013-06-06 7:00:00")
weather_all = weather.archive_update()
# bobo = start_up.start_time(park_ts, city="New_York", state="NY",
#                     date="2013-06-06 7:00:00")

# park_ts_logr = (park_ts / park_ts.shift(1)).apply(sp.log)[1:]
