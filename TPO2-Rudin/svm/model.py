import datetime
import re

import numpy as np
import pandas as pd
import sklearn.grid_search
import sklearn.preprocessing
import sklearn.svm
import sklearn.svm.classes

import ts_proc.munge
import weather.wund

__author__ = 'David Karapetyan'


def _build(endog, weather_orig, cov, gran, params, param_grid, cv, threshold,
           n_jobs, discrete, bin_search):
    """SVM Model Instantiation and Training

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_orig: DataFrame. Built from weather underground data
    :param cov: List of covariates.
    :param gran: Sampling granularity
    :param params: Dictionary of SVM model parameters
    :param param_grid: Dictionary of C and gamma values
    The C and gamma keys point to lists representing initial grids used to find
    the optimal C and gamma
    :param cv: Number of Stratified K-fold cross-validation folds
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

    # get only dates from weather data that coincide with endog dates
    weather_cond = weather.wund.history_munge(df=weather_orig,
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
    y = np.array(endog_filt.astype(int))
    # if 0 and 1s are classed as floats
    # in time series, scikitlearn will complain.
    # Similarly, must reshape to let scikitlearn know we are dealing
    # with multiple samplings, with outputs in 1-space


    if discrete is True:
        svm = sklearn.svm.SVC(**params)

    else:
        svm = sklearn.svm.SVR(**params)

    # get optimal gamma and c
    if bin_search:
        param_grid_opt = _best_params(endog=y, features=x, estimator=svm,
                                      param_grid=param_grid, cv=cv,
                                      n_jobs=n_jobs,
                                      threshold=threshold)
        # refit support vector model with optimal c and gamma
        new_params = params
        new_params["C"] = param_grid_opt["C"]
        new_params["gamma"] = param_grid_opt["gamma"]
        svm.set_params(**new_params)
        # fit the optimal build
        fit = svm.fit(x, y)
    else:
        if type(svm) == sklearn.svm.classes.SVC:
            scofunc = "accuracy"
        elif type(svm) == sklearn.svm.classes.SVR:
            scofunc = "r2"
        else:
            raise ValueError("You have entered an invalid svm. Please use"
                             "an svm of class SVR or SVC")
            # fixed grid search along specified grid
        fit = sklearn.grid_search.GridSearchCV(
                estimator=svm,
                param_grid=param_grid,
                scoring=scofunc,
                cv=cv,
                n_jobs=n_jobs).fit(x, y)
        for item in fit.grid_scores_:
            print(item)
        print("The best parameters are {} with a score of {}".format(
                fit.best_params_, fit.best_score_))

    return [fit, scaler]


def _best_gamma_fit(endog, features, estimator, c, param_grid_gamma, cv, n_jobs,
                    threshold):
    # base case setup
    # initialization to run while loop below at least once (handling the
    # base case at a minimum)
    params = {"C": [c], "gamma": param_grid_gamma}
    score = threshold
    score_next = 3 * threshold
    fit = None

    if type(estimator) == sklearn.svm.classes.SVC:
        scofunc = "accuracy"
    elif type(estimator) == sklearn.svm.classes.SVR:
        scofunc = "r2"
    else:
        raise ValueError("You have entered an invalid estimator. Please use"
                         "an estimator of class SVR or SVC")

    while np.abs(score_next - score) > threshold and score_next > score:
        fit = sklearn.grid_search.GridSearchCV(
                estimator=estimator,
                param_grid=params,
                scoring=scofunc,
                cv=cv,
                n_jobs=n_jobs).fit(features, endog)

        center = fit.best_params_['gamma']
        left = params['gamma'][0]
        right = params['gamma'][-1]
        left_mid = (left + center) / 2
        right_mid = (right + center) / 2
        # check if last element or first element
        # of parameter grid is best. If so, return

        # if left and right is center:
        #     return fit

        # inductive step
        # In the case when right or left equal center, 'set' removes
        # redundant elements
        # sorting done due to weird bug with gridsearch--unsorted
        # grids take longer to process

        left_new_params = {'C': [c],
                           'gamma': sorted({left, left_mid, center})}
        right_new_params = {'C': [c],
                            'gamma': sorted({center, right_mid, right})}

        fit_next_1 = sklearn.grid_search.GridSearchCV(
                estimator=estimator,
                param_grid=left_new_params,
                scoring=scofunc,
                n_jobs=n_jobs).fit(features, endog)

        fit_next_2 = sklearn.grid_search.GridSearchCV(
                estimator=estimator,
                param_grid=right_new_params,
                scoring=scofunc,
                n_jobs=n_jobs).fit(features, endog)

        if fit_next_1.best_score_ <= fit_next_2.best_score_:
            params = right_new_params
            fit_next = fit_next_2
        else:
            params = left_new_params
            fit_next = fit_next_1

        score = fit.best_score_
        score_next = fit_next.best_score_

    return fit


def _best_params(endog, features, estimator, param_grid, cv, n_jobs, threshold):
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
    param_grid_gamma = param_grid["gamma"]
    params = []
    scores = []
    for constant in param_grid["C"]:
        fit = _best_gamma_fit(endog=endog,
                              features=features,
                              estimator=estimator,
                              c=constant,
                              param_grid_gamma=param_grid_gamma,
                              cv=cv,
                              n_jobs=n_jobs,
                              threshold=threshold)
        scores.append(fit.best_score_)
        params.append(fit.best_params_)

    ind = np.argmax(scores)

    collated = params
    for (x, y) in zip(collated, scores):
        x["score"] = y
        print(x)

    print("The best parameters are {} with a score of {}".format(
            params[ind], scores[ind]))

    return params[ind]


def predict(endog, weather_history, weather_forecast, cov, gran,
            params, param_grid, cv, threshold, n_jobs, discrete, bin_search):
    """Time Series Prediciton Using SVM

    :param endog: Series. Endogenous variable to be forecasted
    :param weather_history: Dataframe. Built from weather underground data
    :param weather_forecast: Dataframe. Built from weather underground data
    :param cov: List of covariates
    :param gran: Int. Sampling granularity
    :param params: Dictionary of SVM model parameters
    :param param_grid: Dictionary of grid values for svm C and gamma
    :param cv: Number of Stratified K-fold cross-validation folds
    :param threshold: float. Binary search termination criterion.
    Search over grid terminates if difference of next iteration from current
    does not exceed threshold.
    :param n_jobs: Positive integer specifying number of cores for run
    :param discrete: Boolean identifying whether the endogenous variable
    is discrete or takes a continuum of values
    :param bin_search: Boolean. Whether or not to use binary search along
    gamma grid for each fixed C
    :return: Series
    """
    if discrete is True:
        model, scaler = _build(endog=endog, weather_orig=weather_history,
                               cov=cov, gran=gran, params=params,
                               param_grid=param_grid, cv=cv,
                               threshold=threshold,
                               n_jobs=n_jobs,
                               bin_search=bin_search,
                               discrete=discrete,
                               )

        features = weather.wund.forecast_munge(weather_forecast, gran)[
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
