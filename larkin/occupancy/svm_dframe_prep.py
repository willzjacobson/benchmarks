# coding=utf-8

import datetime
import re

import numpy as np
import sklearn.preprocessing

import larkin.ts_proc.munge
import larkin.weather.mongo


def get_covars(endog, weather_orig, forecast_orig, cov, gran):
    # get weather information

    weather_cond = larkin.weather.wund.history_munge(df=weather_orig,
                                                     gran=gran)[cov]
    forecast_cond = larkin.weather.wund.forecast_munge(df=forecast_orig,
                                                       gran=gran)[cov]

    #########
    # processing for training portion
    #########
    endog_filt = larkin.ts_proc.munge.filter_day_season(endog)
    # only include dates (as integers)that are both in features and
    # endog in training
    # of model
    dates = endog_filt.index.intersection(weather_cond.index)

    endog_filt = endog_filt[dates]
    features_filt = weather_cond.loc[dates]
    # add column with datetime information, sans year or day (convert
    # time since midnight to minutes)
    features_filt = features_filt.reset_index()
    #
    # need granularity as integer, to convert seconds to minutes
    gran_int = int(re.findall('\d+', gran)[0])

    features_filt['index'] = features_filt['index'].apply(
            lambda date:
            datetime.timedelta(hours=date.hour,
                               minutes=date.minute).total_seconds() / gran_int
    )

    scaler = sklearn.preprocessing.MinMaxScaler().fit(features_filt)
    features_filt_scaled = scaler.transform(features_filt)

    x_train = features_filt_scaled
    y_train = np.array(endog_filt.astype(int))

    # if 0 and 1s are classed as floats
    # in time series, scikitlearn will complain.
    # Similarly, must reshape to let scikitlearn know we are dealing
    # with multiple samplings, with outputs in 1-space

    ##########
    #  now prepare forecast features
    ################
    future_features = forecast_cond
    prediction_index = future_features.index
    future_features = future_features.reset_index()

    future_features['time'] = future_features['time'].apply(
            lambda date:
            datetime.timedelta(
                    hours=date.hour,
                    minutes=date.minute).total_seconds() / gran_int
    )

    x_future = scaler.transform(future_features)

    return {"y_train": y_train,
            "x_train": x_train,
            "x_future": x_future,
            "prediction_index": prediction_index,
            "scaler": scaler}
