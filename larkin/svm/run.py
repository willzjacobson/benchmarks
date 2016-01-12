# coding=utf-8
from datetime import datetime

import numpy as np
import pandas as pd
from larkin.svm.model import predict

import __init__

__author__ = 'David Karapetyan'

if __name__ == "__main__":
    # set variables
    params_init = __init__.config["svm"]["params"]
    cov = __init__.config["building_dbs"]["cov"]
    gran = __init__.config["sampling"]["granularity"]
    h5file = __init__.config["building_dbs"]["h5file"]
    history_original_name = __init__.config["building_dbs"]["history_orig"]
    forecast_original_name = __init__.config["building_dbs"]["forecast_orig"]
    store = pd.HDFStore(h5file)
    weather_history = store[history_original_name]
    weather_forecast = store[forecast_original_name]
    store.close()

    granularity = __init__.config["sampling"]["granularity"]
    pg = __init__.config["svm"]["param_search"]["grid"]
    param_grid = {"C": np.logspace(**(pg["C"])),
                  "gamma": np.logspace(**(pg["gamma"])),
                  "kernel": pg["kernel"]}
    threshold = __init__.config["svm"]["param_search"]["threshold"]
    cv = __init__.config["svm"]["param_search"]["cv"]
    n_jobs = __init__.config["svm"]["param_search"]["n_jobs"]

    fandata_store = pd.HDFStore(
            __init__.config["default"]["data_sources"] + "/lex560.h5")
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
    prediction = predict(endog=ts,
                         weather_history=weather_history,
                         weather_forecast=weather_forecast,
                         cov=cov, gran=gran,
                         params=params_init,
                         param_grid=param_grid,
                         cv=cv,
                         threshold=threshold, n_jobs=n_jobs,
                         has_bin_search=False,
                         discrete=True)

    print(prediction)
