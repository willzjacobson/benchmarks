__author__ = 'David Karapetyan'

import weather.helpers
import sklearn.svm
import sklearn.preprocessing
import pandas as pd
import ts_proc.munge
import datetime
import re


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

    if discrete is True:
        # get only dates from weather data that coincide with endog dates
        weather_cond = weather.helpers.history_munge(df=weather_orig,
                                                     gran=gran)[cov]

        endog_filt = ts_proc.munge.filter_day_season(endog)
        # only include dates (as integers)that are both in features and
        # endog in training
        # of model
        dates = endog_filt.index.intersection(weather_cond.index)

        endog_filt = endog_filt[dates]
        features_filt = weather_cond.loc[dates]
        # add column with datetime information, sans year or day (convert
        # time since midnight to minutes)
        features_filt = features_filt.reset_index()

        # need granularity as integer, to convert seconds to minutes
        gran_int = int(re.findall('\d+', gran)[0])

        features_filt['index'] = features_filt['index'].apply(
            lambda date:
            datetime.timedelta(hours=date.hour,
                               minutes=date.minute).total_seconds() / gran_int
        )

        scaler = sklearn.preprocessing.MinMaxScaler().fit(features_filt)
        features_filt_scaled = scaler.transform(features_filt)

        x = features_filt_scaled
        y = endog_filt.astype(int)
        # if 0 and 1s are classed as floats
        # in time series, model will fail

        clf = sklearn.svm.SVC(**params)

        return [clf.fit(x, y), scaler]


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
        model, scaler = _build(endog=endog, weather_orig=weather_history,
                               cov=cov, gran=gran, params=params, discrete=True)

        features = weather.helpers.forecast_munge(weather_forecast, gran)[cov]
        prediction_index = features.index
        features = features.reset_index()

        # need granularity as integer, to convert seconds to minutes
        gran_int = int(re.findall('\d+', gran)[0])

        features['index'] = features['index'].apply(
            lambda date:
            datetime.timedelta(hours=date.hour,
                               minutes=date.minute).total_seconds() / gran_int
        )

        features_scaled = scaler.transform(features)

        predicted_series = pd.Series(
            data=model.predict(features_scaled),
            index=prediction_index)
        return predicted_series
