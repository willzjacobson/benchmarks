# coding=utf-8

import datetime
import re

import ts_proc.munge
import weather.wund


def get_covars(mongo_cred, wund_cred, weather_history_loc, weather_forecast_loc,
               building_ts_loc, granularity):
    weather_orig =
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
