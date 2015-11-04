__author__ = 'David Karapetyan'

import sklearn.svm
import pandas as pd
import numpy as np


def _build(endog, weather_history, cov, params, discrete=True):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_history: DataFrame. Built from weather underground data
    :param cov: List of covariates.
    :param params: Dictionary of SVM model parameters
    :param discrete: Boolean identifying whether the endogenous variable
    is discrete or takes a continuum of values
    :return: Object of Class SVC
    """


    # get weather and endogenous
    # into appropriate format for input to python svm model

    if discrete is True:
        # get only dates from weather data that coincide with endog dates
        weather_cond = weather_history[cov][endog.index[0]:endog.index[-1]]
        # TODO Map Weather Condition to Numbers, to feed into model
        # x is array of arrays. Each entry is a data point from a time series,
        # with its time and weather features

        # master = weather_cond.insert(loc=0, column=endog.name,
        #                             value=endog)

        features = weather_cond.reset_index()
        features['index'] = features['index'].astype(int)

        x = np.array(features)
        y = np.array(endog)
        # x = weather_history.temp.reshape(len(weather_history), 1)

        clf = sklearn.svm.SVC(**params)

        return clf.fit(x, y)


def predict(endog, weather_history, weather_forecast, cov,
            params, discrete=True):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_history: Dataframe. Built from weather underground data
    :param weather_forecast: Dataframe. Built from weather underground data
    :param params: Dictionary of SVM model parameters
    :param discrete: Boolean identifying whether the endogenous variable
    is discrete or takes a continuum of values
    :return: Series
    """
    if discrete is True:
        model = _build(endog=endog, weather_history=weather_history,
                       cov=cov, params=params)

        features = weather_forecast.reset_index()
        features['index'] = features['index'].astype(int)

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
