import os
# set project working directory
os.chdir( '/Users/davidkarapetyan/Documents/workspace/data_analysis/src/park345' )


from park345.custom_fncs import optimal_order
# import IPython
import pandas as pd
# for wide terminal display of pandas dataframes
pd.options.display.width = 120
pd.options.display.max_rows = 10000
import numpy as np
import statsmodels.tsa.arima_model as arima
import statsmodels.tsa.statespace.sarimax as sarimax

# plot inline
# IPython.get_ipython().magic('matplotlib inline')
import matplotlib.pylab as pylab

pylab.rcParams['figure.figsize'] = 14, 6








# load dataframe, and subset out relevant columns
park_data = pd.read_csv( 'data/park345_steam.csv', error_bad_lines = False )
park_data = park_data.loc[:, ['TIMESTAMP', 'VALUE']]
park_data = park_data.sort( 'TIMESTAMP' )


# construct time series, getting rid of microseconds
park_ts = pd.Series( list( park_data.VALUE ),
                    pd.DatetimeIndex( park_data.TIMESTAMP ),
                    name = "steam values" )

park_ts = park_ts.loc[park_ts != 0].resample( '15Min ', fill_method = 'pad' )
print( park_ts )

arima.ARIMA( park_ts, optimal_order( park_ts ) ).fit().summary()


# We see that ARIMA is not currently fitting the time series data. We look for
# an appropriate transformation of the time series to improve our ARIMA fitting.

# ###Log Ratio Transformation



park_ts_logr = ( np.log( park_ts / park_ts.shift( 1 ) ) )[1:]


# To get a properly scaled plot, we filter out the outlier values occuring at
#  the end of day (shift from some steam usage to none at all as systems
#  restart, and spikes from ramp-up time at the beginning of the day).

park_ts_logr.describe( percentiles = [0.05, 0.95] )

park_ts_logr[( park_ts_logr > 0.001 ) & ( park_ts_logr < 0.23 )][
'2013-05-01': '2013-05-15'].plot()


# The seasonality is clear. We now plot a single day, filtering out
#  outliers to get a properly scaled figure.



park_ts_logr[( park_ts_logr > 0.005 ) & ( park_ts_logr < 0.18 )][
    '2013-05-15'].plot()


# Next, we utilise a SARIMAX model, with seasonality at 96
#  (our data points are spaced at 15 minute intervals),
#  and analyze a week's worth of data (starting on Monday, and ending on Friday).



park_fit_week = sarimax.SARIMAX( park_ts_logr.loc['2013-05-06':'2013-05-10'],
                                seasonal_order = ( 0, 1, 0, 96 ) ).fit().summary()


# While the fit isn't terrible, it can be improved by first observing
# that we have spikes in our at the beginning of the day. This is due to
# the ratio of chilled water temperature dipping suddenly at the end of day
# as systems are ramped down.
# Observe that the only negative values in the data occur at the start of
#  day. We filter these out, and re-run SARIMA.



sarimax.SARIMAX( 
    park_ts_logr[park_ts_logr > 0]['2013-05-06':'2013-05-10'],
    seasonal_order = ( 0, 1, 0, 95 ) ).fit().summary()


# Observe that the sarimax model seems to fit nicely now that we have
# filtered out the beginning-of-day spike. Now, let's use a larger input
# (beginning on a Monday, and ending on a Friday), and fit another
# Sarimax model to our beginning-of-day spike-filtered data.



sarimax.SARIMAX( 
    park_ts_logr[park_ts_logr > 0]['2013-05-06':'2013-06-07'],
    seasonal_order = ( 0, 1, 0, 95 ) ).fit().summary()


# This is an even better fit than the fit for the week's worth of data.
# Lastly, we input three # months worth of data, beginning on a Monday,
# and ending on a Friday.



sarimax.SARIMAX( park_ts_logr[park_ts_logr > 0]['2013-05-06': '2013-08-08'],
                seasonal_order = ( 0, 1, 0, 95 ) ).fit().summary()


# Let's contrast this with our fit when we include the end-of-day spikes:



sarimax.SARIMAX( park_ts_logr['2013-05-06': '2013-08-08'],
                seasonal_order = ( 0, 1, 0, 96 ) ).fit().summary()


# The excellent fit for even a large data set after filtering the ramp-up
# and ramp-down 15 minute spikes, and the poor fit when we keep them in,
# suggests that, apart from ramp-up and ramp-down times, the behavior of
# chilled water temperate is strongly linear. A possible future line of
# research is to investigate seasonality on a monthly level (for example,
# analyzing data in chunks of winter, spring, summer, fall), and so on, in
# order to attempt further improve fit.
#
# However, from the looks of the data, it makes sense to keep the analysis of
# 15-minute ramp-up and ramp-down times separate from all other data.




# ##SARIMAX on Data for Individual Days

# We next investigate seasonality on a weekly basis. That is, we
# isolate the 5-day workweek into 5 chunks, and run SARIMAX on
# each chunk separately.




sarimax.SARIMAX( park_ts_logr[np.logical_and( park_ts_logr.index.weekday == 0,
                                             park_ts_logr > 0 )],
                seasonal_order = ( 0, 1, 0, 95 ) ).fit().summary()


# As expected, the fit is good, but not as good as for our data set considering
# all days of the week. We suspect that this is due to there being fewer data
# points in the SARIMAX fitting above. To remedy this, we re-run SARIMAX on a
# larger data set of Mondays.



sarimax.SARIMAX( park_ts_logr[ np.logical_and( park_ts_logr.index.weekday == 0,
                             park_ts_logr > 0 )]['2013-03':'2014-02'],
                seasonal_order = ( 0, 1, 0, 95 ) ).fit().summary()


# We do the same for Tuesdays, Wednesdays, etc.



sarimax.SARIMAX( park_ts_logr[ np.logical_and( park_ts_logr.index.weekday == 1,
                             park_ts_logr > 0 )]['2013-03':'2014-02'],
                seasonal_order = ( 0, 1, 0, 95 ) ).fit().summary()




# SARIMAX(0,1,0,95) MLE estimator doesn't converge

sarimax.SARIMAX( park_ts_logr[ np.logical_and( park_ts_logr.index.weekday == 2,
                             park_ts_logr > 0 )]['2013-03':'2014-02'],
                seasonal_order = ( 0, 1, 0, 95 ) ).fit().summary()

sarimax.SARIMAX( park_ts_logr[ np.logical_and( park_ts_logr.index.weekday == 3,
                             park_ts_logr > 0 )]['2013-03':'2014-02'],
                seasonal_order = ( 0, 1, 0, 95 ) ).fit().summary()

sarimax.SARIMAX( park_ts_logr[ np.logical_and( park_ts_logr.index.weekday == 4,
                             park_ts_logr > 0 )]['2013-03':'2014-02'],
                seasonal_order = ( 0, 1, 0, 95 ) ).fit().summary()


# ##ARIMAX For Ramp-up and Ramp-Down

# We shall treat Monday ramp-ups separately from the remaining days of the week,
# due to difference between system-idling over weekends and weekdays.



arima.ARIMA( park_ts_logr[ np.logical_and( park_ts_logr.index.weekday == 0,
                             park_ts_logr < 0 )], order = ( 0, 1, 0 ) ).fit().summary()


# Observe that between end of day and start of day, chilled water temperature
# decreases, and so $$\frac{T_k(0 + 00:15)}{T_k(0)} = a_k < 1$$ for each
# entry in our training set. The set $\{a_k\}_k$ will hopefully consist of
#  entries that are clustered near one another, with some reasonable volatility.
#  Taking a logarithm of them will result in an exponential increase in
#  volatility, since $log(x)$ is an exponential function of $x$ for decreasing
#  $x < 1$. This will result in decreasing the goodness-of-fit of a linear
#  model, from a least-squares standpoint. Consequently, we exponentiate our
#  time series data, and re-fit:
arima.ARIMA( np.exp( park_ts_logr[ np.logical_and( park_ts_logr.index.weekday == 0,
                             park_ts_logr < 0 )] ), order = ( 0, 1, 0 ) ).fit().summary()



# Observe that the fit has improved dramatically.
