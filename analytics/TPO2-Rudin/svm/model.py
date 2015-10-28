__author__ = 'davidkarapetyan'

import sklearn
from dateutil.relativedelta import relativedelta
import pandas as pd
import config


def model_build(endog,
                weather_archive,
                params=config.david["svm"]):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_archive: DataFrame. Built from weather underground data
    :param params: Dictionary of SVM model parameters
    :return: Object of Class SVC
    """


    # get weather and endogenous
    # into appropriate format for input to python svm model

    number_points = 60 / params.sampling.forecast_granularity * 24

    x = weather_archive.temp.reshape(1, number_points)
    y = list(endog)

    clf = sklearn.svm.SVC()
    return clf.fit(x, y, *params)


def model_predict(endog,
                  weather_archive,
                  weather_forecast,
                  params=config.david["svm"]):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_archive: Dataframe. Built from weather underground data
    :param weather_forecast: Dataframe. Built from weather underground data
    :param params: Dictionary of SVM model parameters
    :return: Time Series
    """

    model = model_build(endog=endog, weather_archive=weather_archive,
                        params=params)
    number_points = 60 / params.sampling.forecast_granularity * 24
    x = weather_forecast.temp.reshape(1, number_points)

    times_forecast = pd.date_range(endog.index[-1] + relativedelta('15min'),
                                   endog.index[-1].date() + relativedelta(
                                       days=1),
                                   freq='15min')

    predicted_series = pd.Series(data=model.predict(x), index=times_forecast)
    return predicted_series
