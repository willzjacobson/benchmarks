# coding: utf-8

import pandas as pd
# for wide terminal display of pandas dataframes
pd.options.display.width = 120
pd.options.display.max_rows = 10000
import statsmodels.tsa.arima_model as arima
# from IPython import get_ipython
import statsmodels.graphics.tsaplots as tsp
import scipy as sp
from custom_fncs.misc import *
# %load_ext autoreload #reload functions within modules automatically

# plot inline
# get_ipython().magic('pylab inline')
# IPython.get_ipython().magic('matplotlib inline')

# plt.rcParams['figure.figsize'] = 14, 6

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

park_ts.drop_duplicates(inplace=True)
park_ts = park_ts.loc[park_ts != 0].resample('15Min ').interpolate()

park_ts_logr = (park_ts / park_ts.shift(1)).apply(sp.log)[1:]

'''
##SARIMAX on Data for Individual Days

We next investigate seasonality on a weekly basis. That is, we
isolate the 5-day workweek into 5 chunks, and run SARIMAX on
each chunk separately.

'''

print(park_ts_logr['06-01-2013':'07-01-2013'])

'''
From June to July, there is an interesting discrepancy. It seems the operators
are powering up the system at 8:00am, after a gradual ramp down before.
We suspect this is due to operator error, or to a bad DiBoss summertime
prediction.
 '''

# TODO Check 06-07 non-steady ramp up/down with Gene.
# Maybe bad DiBoss summertime predictions

tsp.plot_acf(park_ts['06-04-2013'])
tsp.plot_pacf(park_ts['06-04-2013'])

tsp.plot_acf(park_ts.at_time('10:30:00'))
tsp.plot_pacf(park_ts.at_time('10:30:00'))
#
# actual_vs_prediction(park_ts)
stationarity_test(park_ts['06-01-2013':'07-01-2013'])
actual_vs_prediction(park_ts['06-01-2013':'07-01-2013'])
actual_vs_prediction(park_ts['06-01-2013':'06-06-2013'], (0, 1, 0, 96))

'''
##ARIMAX For Ramp-up and Ramp-Down

We shall treat Monday ramp-ups separately from the remaining days of the week,
due to difference between system-idling over weekends and weekdays.

'''
print(arima.ARIMA(park_ts_logr[sp.logical_and(park_ts_logr.index.weekday == 0,
                                              park_ts_logr < 0)],
                  order=(0, 1, 0)).fit().summary())

'''
Observe that between end of day and start of day, chilled water temperature
decreases, and so $$\frac{T_k(0 + 00:15)}{T_k(0)} = a_k < 1$$ for each
entry in our training set. The set $\{a_k\}_k$ will hopefully consist of
entries that are clustered near one another, with some reasonable volatility.
Taking a logarithm of them will result in an exponential increase in
volatility, since $log(x)$ is an exponential function of $x$ for decreasing
$x < 1$. This will result in decreasing the goodness-of-fit of a linear
model, from a least-squares standpoint. Consequently, we exponentiate our
time series data, and re-fit:
'''

print(arima.ARIMA(
    (park_ts_logr[sp.logical_and(park_ts_logr.index.weekday == 0,
                                 park_ts_logr < 0)]).apply(sp.exp),
    order=(0, 1, 0)).fit().summary())

'''
Observe that the fit has improved.
'''
