directory = '/Users/davidkarapetyan/Documents/workspace/data_analysis/'
csv_file = 'data/park345_oa_temp.csv'

import pandas as pd
# for wide terminal display of pandas dataframes
pd.options.display.width = 120
pd.options.display.max_rows = 10000
import sklearn.cluster as cluster
from sklearn.neighbors.kde import KernelDensity
from scipy import stats
import numpy as np
import statsmodels.tsa.arima_model as arima
import statsmodels.tsa.statespace.sarimax as sarimax

# plot inline
# %pylab inline
# IPython.get_ipython().magic('matplotlib inline')
import matplotlib.pylab as pylab

pylab.rcParams['figure.figsize'] = 14, 6


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
park_ts.drop_duplicates(inplace=True)
park_ts = park_ts.loc[park_ts != 0].resample('15Min ').interpolate()

print(park_ts)

pylab.scatter(park_ts['2013-03-21': '2013-05-27'].index.minute / 15,
              park_ts['2013-03-21': '2013-05-27'].values
              )

density = stats.kde.gaussian_kde(park_ts['2013-03-21': '2013-08-27'].values)

pylab.plot(park_ts['2013-03-21': '2013-08-27'].values,
           density(park_ts['2013-03-21': '2013-08-27'].values))

kde = KernelDensity(kernel='gaussian', bandwidth=0.1).fit(park_ts['2013-03-21': '2013-08-27'].values)
