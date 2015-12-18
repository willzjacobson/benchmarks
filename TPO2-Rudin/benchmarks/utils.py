# coding=utf-8

import pandas as pd

import weather.mongo
import weather.wund

__author__ = 'ashishgagneja'


def _filter_missing_weather_data(weather_df):
    """
    Filter/remove rows with missing data like -9999's

    :param weather_df: pandas DataFrame
    :return: pandas DataFrame
    """

    # TODO: it might be better not to ignore good data in records with
    # some missing data
    bad_data = weather_df.where(weather_df < -998).any(axis=1)
    return weather_df.drop(bad_data[bad_data == True].index)



def get_weather(host, port, username, password, source_db, history_db,
                 history_collection, forecast_db, forecast_collection, gran):
    """ Load all available weather data, clean it and drop unneeded columns

    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file
    :param gran: int
        sampling frequency of input data and forecast data

    :return: pandas DataFrame
    """


    # TODO: this should be done before munging for efficiency

    hist = weather.mongo.get_history(host, port, source_db, history_db,
                                      username, password, history_collection)
    # print(hist.axes)
    hist_munged = (weather.wund.history_munge(hist, gran))['wetbulb']

    fcst = weather.mongo.get_latest_forecast(host, port, source_db, forecast_db,
                                             username, password,
                                             forecast_collection)
    # print(fcst.axes)
    fcst_munged = (weather.wund.forecast_munge(fcst, gran))['wetbulb']

    # concatenate history and forecast into one series; prefer history over
    # forecast, if overlapping
    fcst_only_idx = fcst_munged.index.difference(hist_munged)
    wetbulb_ts = pd.concat([hist_munged, fcst_munged.loc[fcst_only_idx]])

    return wetbulb_ts.dropna()