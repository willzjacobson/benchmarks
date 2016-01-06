# coding=utf-8
from datetime import datetime

import numpy as np
import pandas as pd

import config
import svm.model

__author__ = 'David Karapetyan'

if __name__ == "__main__":
    # set variables
    params_init = config.config["svm"]["params"]
    cov = config.config["building_dbs"]["cov"]
    gran = config.config["sampling"]["granularity"]
    h5file = config.config["building_dbs"]["h5file"]
    history_original_name = config.config["building_dbs"]["history_orig"]
    forecast_original_name = config.config["building_dbs"]["forecast_orig"]
    store = pd.HDFStore(h5file)
    weather_history = store[history_original_name]
    weather_forecast = store[forecast_original_name]
    store.close()

    granularity = config.config["sampling"]["granularity"]
    pg = config.config["svm"]["param_search"]["grid"]
    param_grid = {"C": np.logspace(**(pg["C"])),
                  "gamma": np.logspace(**(pg["gamma"])),
                  "kernel": pg["kernel"]}
    threshold = config.config["svm"]["param_search"]["threshold"]
    cv = config.config["svm"]["param_search"]["cv"]
    n_jobs = config.config["svm"]["param_search"]["n_jobs"]

    fandata_store = pd.HDFStore(
            config.config["default"]["data_sources"] + "/lex560.h5")
    fandata = fandata_store.bms_hva_fan
    fandata_store.close()
    cleandata = fandata[(fandata.FLOOR == 'F02') & (fandata.ZONE == 'Z00')]

    # construct endogenous variable to run predictions on

    date_objects = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in
                    cleandata.TIMESTAMP]

    ts = pd.Series(data=list(cleandata.VALUE),
                   index=date_objects)
    ts = ts.resample(granularity).fillna(method="bfill")

    # run prediction
    prediction = svm.model.predict(y_train=ts,
                                   weather_history=weather_history,
                                   weather_forecast=weather_forecast,
                                   cov=cov, gran=gran,
                                   params=params_init,
                                   param_grid=param_grid,
                                   cv=cv,
                                   threshold=threshold, n_jobs=n_jobs,
                                   bin_search=False,
                                   discrete=True)

    print(prediction)
