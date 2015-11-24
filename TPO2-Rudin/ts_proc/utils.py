from IPython.parallel import Client

rc = Client()
dview = rc[:]
dview.block = True

with dview.sync_imports():
    from statsmodels.tsa.arima_model import ARIMA
    from scipy.optimize import brute
    import numpy as np
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    sns.set()


def optimal_order(ts):
    """Outputs optimal Arima order for an input time series.

    :param ts: pandas.core.series.Series
    :return: tuple
    """

    return tuple(
        map(int,
            brute(lambda x: ARIMA(ts, x).fit().aic,
                  ranges=(slice(0, 2, 1),
                          slice(0, 2, 1),
                          slice(0, 2, 1)),
                  finish=None)
            )
    )


def ts_day_pos(ts, day, time, start, end, freq):
    """Returns slice of input time series

    Time series subset consists of all points at a specific time between
    start and end dates, and sampled with an input frequency

    :param ts: pandas.core.series.Series
    :param day: int
    Day of week
    :param time: datetime.datetime
    Time of day. Defaults to None
    :param start: datetime.datetime
    :param end: datetime.datetime
    :param freq: frequency alias
    :return: pandas.core.series.Series
    """
    temp = ts[pd.date_range(start=start, end=end, freq=freq)]
    temp = temp[temp.index.weekday == day]

    if time is None:
        return temp
    else:
        return temp.at_time(time)


def filter_two_std(ts):
    stats = ts.describe(percentiles=[.05, .95])
    low, high = stats['5%'], stats['95%']
    return ts[ts.between(low, high)]


def actual_vs_prediction(ts, order=(1, 1, 0), seasonal_order=(1, 1, 0, 96),
                         days=(0, 1, 2, 3, 4, 5, 6)):
    """Plots SARIMA predictions against real values for each weekday.

    :param ts: pandas.core.series.Series
    :param order: tuple
    :param seasonal_order: tuple
    :param days: tuple
    :return: None
    """
    days_length = len(days)
    if days_length > 2:
        nrows = int(np.ceil(days_length / 2))
        ncols = 2

    else:
        ncols = days_length
        nrows = 1

    fig, ax = plt.subplots(nrows, ncols, squeeze=False)

    if nrows * ncols > days_length:
        fig.delaxes(ax[nrows - 1, ncols - 1])  # one more plot than needed

    fig.suptitle('In-sample Prediction vs Actual')
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                4: 'Friday',
                5: 'Saturday', 6: 'Sunday'}
    title = ts.name

    fit_list = dview.map_sync(lambda x:
                              SARIMAX(
                                  ts[ts.index.weekday == x],
                                  order=order,
                                  seasonal_order=seasonal_order).fit(), days)

    fit_dict = {day: fit_list[index] for (index, day) in enumerate(days)}

    days_iter = iter(days)
    day = next(days_iter, None)
    for axrow in ax:
        for i in range(ncols):
            if day is not None:
                fit = fit_dict[day]
                axrow[i].set_title(weekdays[day])
                axrow[i].plot(ts.index, ts.values,
                              label='Actual')
                ts_fit = pd.Series(data=fit.predict().flatten(),
                                   index=fit.data.dates)
                ts_fit_filtered = filter_two_std(ts_fit)
                axrow[i].plot(ts_fit_filtered.index, ts_fit_filtered.values,
                              label='Prediction')
                axrow[i].legend(loc='best')
                axrow[i].set_ylabel(title)
                day = next(days_iter, None)
    plt.show()
    plt.draw()
    plt.tight_layout()  # doesn't work without plt.draw coming before
