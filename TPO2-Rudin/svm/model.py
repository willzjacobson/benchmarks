import datetime
import re

import numpy as np
import pandas as pd
import sklearn

import ts_proc.munge
import weather.helpers

__author__ = 'David Karapetyan'


def _build(endog, weather_orig, cov, gran, params, param_grid, threshold,
           n_jobs,
           discrete=True):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_orig: DataFrame. Built from weather underground data
    :param cov: List of covariates.
    :param gran: Sampling granularity
    :param params: Dictionary of SVM model parameters
    :param param_grid: Dictionary of C and gamma values
    The C and gamma keys point to lists representing initial grids used to find
    the optimal C and gamma
    :param threshold: float. Binary search termination criterion.
    Search over grid terminates if difference of next iteration from current
    does not exceed threshold.
    :param discrete: Boolean.
    Identifies whether the endogenous variable
    is discrete or takes a continuum of values
    :return: List of objects.
    One contains the fitted model, the other the data
    normalization scaling parameters
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

        x = features_filt_scaled
        y = endog_filt.astype(int)
        # if 0 and 1s are classed as floats
        # in time series, model will fail

        svr = sklearn.svm.SVC(**params)

        param_grid_opt = _best_params(svr, param_grid, n_jobs, threshold)
        clf = sklearn.grid_search.GridSearchCV(estimator=svr,
                                               param_grid=param_grid_opt,
                                               n_jobs=n_jobs)

        fit = clf.fit(x, y)

        return [fit, scaler]


def _best_gamma(estimator, c, param_grid_gamma, n_jobs, threshold):
    fit = sklearn.grid_search.GridSearchCV(estimator,
                                           param_grid_gamma,
                                           n_jobs).fit()

    if param_grid_gamma[0] or param_grid_gamma[-1] is \
            fit.best_params_[
                'gamma']:
        return fit.best_params_

    center = fit.best_params_['gamma']
    left = param_grid_gamma[0]
    right = param_grid_gamma[-1]
    left_mid = (param_grid_gamma[0] + center) / 2
    right_mid = (param_grid_gamma[-1] + center) / 2

    left_new_params = {'C': c, 'gamma': [left, left_mid, center]}
    right_new_params = {'C': c, 'gamma': [center, right_mid, right]}

    fit_next_1 = sklearn.grid_search.GridSearchCV(estimator,
                                                  left_new_params,
                                                  n_jobs).fit()

    fit_next_2 = sklearn.grid_search.GridSearchCV(estimator,
                                                  right_new_params,
                                                  n_jobs).fit()

    if fit_next_1.best_score_ <= fit_next_2.best_score:
        new_params = right_new_params
        fit_next = fit_next_2
    else:
        new_params = left_new_params
        fit_next = fit_next_1

    # base case:
    if fit_next.best_score_ <= fit.best_score:
        return fit.best_params_

    # inductive step
    while np.abs(fit_next.best_score_ - fit.best_score_) > threshold:
        # check if last element or first element
        # of parameter grid is best. If so, return
        # check if last element or first element
        # of parameter grid is best. If so, return

        fit = sklearn.grid_search.GridSearchCV(estimator,
                                               new_params,
                                               n_jobs).fit()

        if new_params['gamma'][-1] is fit.best_params_['gamma']:
            return param_grid_gamma

        center = new_params[1]
        left = new_params[0]
        right = new_params[2]
        left_mid = (new_params[0] + new_params[1]) / 2
        right_mid = (new_params[1] + new_params[2]) / 2

        left_new_params = {'C': c, 'gamma': [left, left_mid, center]}
        right_new_params = {'C': c, 'gamma': [center, right_mid, right]}

        fit_next_1 = sklearn.grid_search.GridSearchCV(estimator,
                                                      left_new_params,
                                                      n_jobs).fit()

        fit_next_2 = sklearn.grid_search.GridSearchCV(estimator,
                                                      right_new_params,
                                                      n_jobs).fit()

        if fit_next_1.best_score_ <= fit_next_2.best_score:
            new_params = right_new_params
            fit_next = fit_next_2
        else:
            new_params = left_new_params
            fit_next = fit_next_1

        if fit_next.best_score_ <= fit.best_score:
            return fit


def _best_params(estimator, param_grid, n_jobs, threshold):
    """
    Function returning a dictionary of the optimal SVM C and gamma
    parameters

    :param estimator: The scikit-learn model class.
    Example: SVC
    :param param_grid: Dictionary of initial C and gamma grid.
    Optimization is done over this grid using binary search
    :param n_jobs: Number of processors for run
    :param threshold: Binary search termination criterion.
    Search terminates if difference of next iteration from current
    does not exceed threshold.
    :return: Dictionary of optimal C and gamma values for SVM run
    """
    params = []
    scores = []
    for constant in param_grid["C"]:
        fit = _best_gamma(estimator, constant, param_grid, n_jobs,
                          threshold)
        scores.append(fit.best_score_)
        params.append(fit.best_params_)

    ind = np.argmax(scores)

    return params[ind]


def predict(endog, weather_history, weather_forecast, cov, gran,
            params, param_grid, threshold, n_jobs, discrete=True):
    """Time Series Prediciton Using SVM

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_history: Dataframe. Built from weather underground data
    :param weather_forecast: Dataframe. Built from weather underground data
    :param cov: List of covariates
    :param gran: Int. Sampling granularity
    :param params: Dictionary of SVM model parameters
    :param param_grid: Dictionary of grid values for svm C and gamma
    :param threshold: float. Binary search termination criterion.
    Search over grid terminates if difference of next iteration from current
    does not exceed threshold.
    :param n_jobs: Positive integer specifying number of cores for run
    :param discrete: Boolean identifying whether the endogenous variable
    is discrete or takes a continuum of values
    :return: Series
    """
    if discrete is True:
        model, scaler = _build(endog=endog, weather_orig=weather_history,
                               cov=cov, gran=gran, params=params,
                               param_grid=param_grid, threshold=threshold,
                               n_jobs=n_jobs,
                               discrete=discrete)

        features = weather.helpers.forecast_munge(weather_forecast, gran)[
            cov]
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
