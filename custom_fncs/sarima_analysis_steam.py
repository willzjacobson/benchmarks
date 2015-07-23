# coding: utf-8

import pandas as pd
# for wide terminal display of pandas dataframes
pd.options.display.width = 120
pd.options.display.max_rows = 10000
import numpy as np
import statsmodels.tsa.arima_model as arima
import statsmodels.tsa.statespace.sarimax as sarimax
import seaborn as sns
import matplotlib.pyplot as plt
# from IPython import get_ipython
import statsmodels.graphics.tsaplots as tsp

# plot inline
# get_ipython().magic('pylab inline')
# IPython.get_ipython().magic('matplotlib inline')

# plt.rcParams['figure.figsize'] = 14, 6
sns.set()

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

park_ts_logr = (np.log(park_ts / park_ts.shift(1)))[1:]




'''
##SARIMAX on Data for Individual Days

We next investigate seasonality on a weekly basis. That is, we
isolate the 5-day workweek into 5 chunks, and run SARIMAX on
each chunk separately.

'''

print(park_ts_logr['06-01-2013':'07-01-2013'])

'''
From June to July, there is an interesting discrepancy. It seems the operators are powering up
the system at 8:00am, after a gradual ramp down before. We suspect this is due to operator error,
or to a bad DiBoss summertime prediction.
 '''


#TODO Check 06-07 non-steady ramp up/down with Gene. Maybe bad DiBoss summertime predictions





def actual_vs_prediction(ts, seasonal_order, tuple=(0, 1, 2, 3, 4, 5, 6), columns=2):
    ncols = 1
    nrows = 1
    fig, ax = plt.subplots(nrows, ncols, squeeze=False)
    # fig.delaxes(ax[3, 1]) #one more plot axes than is needed
    fig.suptitle('Insample Prediction vs Actuals')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    k = 0
    for axentry in ax:
        for i in range(ncols):
            if k < 1:
                ts_within_day = ts[ts.index.weekday == k]
                # stats = ts_within_day.describe(percentiles=[0.05, 0.95])
                # fit = sarimax.SARIMAX(ts_within_day[ts_within_day > stats['5%']],
                # seasonal_order=seasonal_order).fit()
                fit = sarimax.SARIMAX(ts_within_day, order=(2, 1, 0), seasonal_order=seasonal_order).fit()
                # axentry[i].set_title(days[tuple[k]])
                axentry[i].plot(fit.data.dates, fit.data.endog.flatten(), label='Actual')
                axentry[i].plot(fit.data.dates, fit.predict().flatten(), label='Prediction')
                axentry[i].legend(loc='best')
                axentry[i].set_xlabel('')
                axentry[i].set_ylabel('Steam Log Ratios')
                k = k + 1
    plt.show()


tsp.plot_acf(park_ts['06-04-2013'])
tsp.plot_pacf(park_ts['06-04-2013'])

tsp.plot_acf(park_ts.at_time('10:30:00'))
tsp.plot_pacf(park_ts.at_time('10:30:00'))

actual_vs_prediction(park_ts, (2, 1, 0, 96))
actual_vs_prediction(park_ts['06-01-2013':'07-01-2013'], (2, 1, 0, 96))
actual_vs_prediction(park_ts['06-01-2013':'06-06-2013'], (0, 1, 0, 96))

print(sarimax.SARIMAX(park_ts_logr[np.logical_and(park_ts_logr.index.weekday == 1,
                                                  park_ts_logr > basic_stats['5%'])],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

print(sarimax.SARIMAX(park_ts_logr[np.logical_and(park_ts_logr.index.weekday == 2,
                                                  park_ts_logr > basic_stats['5%'])],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

print(sarimax.SARIMAX(park_ts_logr[np.logical_and(park_ts_logr.index.weekday == 3,
                                                  park_ts_logr > basic_stats['5%'])],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

print(sarimax.SARIMAX(park_ts_logr[np.logical_and(park_ts_logr.index.weekday == 4,
                                                  park_ts_logr > basic_stats['5%'])],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

print(sarimax.SARIMAX(park_ts_logr[np.logical_and(park_ts_logr.index.weekday == 5,
                                                  park_ts_logr > basic_stats['5%'])],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

print(sarimax.SARIMAX(park_ts_logr[park_ts_logr.index.weekday == 0],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

print(sarimax.SARIMAX(park_ts_logr[park_ts_logr.index.weekday == 1],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

print(sarimax.SARIMAX(park_ts_logr[park_ts_logr.index.weekday == 2],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

print(sarimax.SARIMAX(park_ts_logr[park_ts_logr.index.weekday == 3],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

print(sarimax.SARIMAX(park_ts_logr[park_ts_logr.index.weekday == 4],
                      seasonal_order=(0, 1, 0, 95)).fit().summary())

'''
##ARIMAX For Ramp-up and Ramp-Down

We shall treat Monday ramp-ups separately from the remaining days of the week,
due to difference between system-idling over weekends and weekdays.

'''

print(arima.ARIMA(park_ts_logr[np.logical_and(park_ts_logr.index.weekday == 0,
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

print(arima.ARIMA(np.exp(park_ts_logr[np.logical_and(park_ts_logr.index.weekday == 0,
                                                     park_ts_logr < 0)]),
                  order=(0, 1, 0)).fit().summary())

'''
Observe that the fit has improved.
'''
