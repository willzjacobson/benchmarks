__author__ = 'davidkarapetyan'

import sklearn.svm
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import config


def _build(endog, weather_archive, params, discrete=True):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_archive: DataFrame. Built from weather underground data
    :param params: Dictionary of SVM model parameters
    :param discrete: Boolean identifying whether the endogenous variable
    is discrete or takes a continuum of values
    :return: Object of Class SVC
    """


    # get weather and endogenous
    # into appropriate format for input to python svm model

    if discrete is True:
        cov = config.david["weather"]["cov"]
        # get only dates from weather data that coincide with endog dates
        weather_cond = weather_archive[cov][endog.index[0]:endog.index[-1]]

        x = np.array(weather_cond.insert(loc=0, column=endog.name, value=endog))
        # x = weather_archive.temp.reshape(len(weather_archive), 1)
        y = list(endog)

        clf = sklearn.svm.SVC(**params)

        return clf.fit(x, y)


def predict(endog, weather_archive, weather_forecast,
            params, granularity, discrete=True):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_archive: Dataframe. Built from weather underground data
    :param weather_forecast: Dataframe. Built from weather underground data
    :param params: Dictionary of SVM model parameters
    :param granularity: Frequency (in minutes) of endog
    :param discrete: Boolean identifying whether the endogenous variable
    is discrete or takes a continuum of values
    :return: Series
    """
    if discrete is True:
        model = _build(endog=endog, weather_archive=weather_archive,
                       params=params)
        number_points = 60 / granularity * 24

        features = weather_forecast.temp.reshape(1, number_points)

        gran_string = str(granularity) + "min"

        times_forecast = pd.date_range(
            endog.index[-1] + relativedelta(gran_string),
            endog.index[-1].date() + relativedelta(
                days=1),
            freq=gran_string)

        predicted_series = pd.Series(data=model.predict(features),
                                     index=times_forecast)
        return predicted_series
