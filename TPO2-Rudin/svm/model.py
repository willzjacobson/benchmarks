__author__ = 'David Karapetyan'

import weather.helpers
import sklearn.svm
import pandas as pd
import numpy as np
import ts_proc.munge


def _build(endog, weather_orig, cov, gran, params, discrete=True):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_orig: DataFrame. Built from weather underground data
    :param cov: List of covariates.
    :param gran: Sampling granularity
    :param params: Dictionary of SVM model parameters
    :param discrete: Boolean identifying whether the endogenous variable
    is discrete or takes a continuum of values
    :return: Object of Class SVC
    """

    # seasons = config.david["weather"]["seasons"]

    # get weather and endogenous
    # into appropriate format for input to python svm model

    if discrete is True:
        # get only dates from weather data that coincide with endog dates
        weather_cond = weather.helpers.history_munge(df=weather_orig, cov=cov,
                                                     gran=gran)
        # TODO Map Weather Condition to Numbers, to feed into model
        # x is array of arrays. Each entry is a data point from a time series,
        # with its time and weather features

        # master = weather_cond.insert(loc=0, column=endog.name,
        #                             value=endog)

        endog_filt = ts_proc.munge.filter_day_season(endog)
        # only include dates (as integers)that are both in features and
        # endog in training
        # of model
        dates = endog_filt.index.intersection(weather_cond.index)

        endog_filt = endog_filt[dates]
        features_filt = weather_cond.loc[dates]
        # add column with datetime information, sans year (just have epoch year
        # as dummy year placeholder entry)
        features_filt = features_filt.reset_index()
        features_filt['index'] = features_filt['index'].apply(
            lambda date: pd.datetime(1970, date.month, date.day, date.hour,
                                     date.minute))
        # convert to epoch
        features_filt['index'] = features_filt['index'].astype(np.int64)

        x = np.array(features_filt)
        y = np.array(endog_filt)
        # x = weather_orig.temp.reshape(len(weather_orig), 1)

        clf = sklearn.svm.SVC(**params)

        return clf.fit(x, y)


def predict(endog, weather_history, weather_forecast, cov, gran,
            params, discrete=True):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_history: Dataframe. Built from weather underground data
    :param weather_forecast: Dataframe. Built from weather underground data
    :param cov: List of covariates
    :param gran: Int. Sampling granularity
    :param params: Dictionary of SVM model parameters
    :param discrete: Boolean identifying whether the endogenous variable
    is discrete or takes a continuum of values
    :return: Series
    """
    if discrete is True:
        model = _build(endog=endog, weather_orig=weather_history,
                       cov=cov, gran=gran, params=params)

        features = weather_forecast[cov].reset_index()
        features['index'] = features['index'].apply(
            lambda date: pd.datetime(1970, date.month, date.day, date.hour,
                                     date.minute)).astype(np.int64)

        # number_points = 60 / granularity * 24
        # features = weather_forecast.temp.reshape(1, number_points)

        # times_forecast = pd.date_range(
        #     endog.index[-1] + relativedelta(granularity),
        #     endog.index[-1].date() + relativedelta(
        #         days=1),
        #     freq=granularity)

        predicted_series = pd.Series(data=model.predict(features),
                                     index=weather_forecast.index)
        return predicted_series
