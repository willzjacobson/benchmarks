__author__ = 'davidkarapetyan'

import pandas as pd

import svm.model
import config

if __name__ == "__main__":
    # set variables

    weather_history = pd.read_hdf(config.david["weather"]["h5file"],
                                  config.david["weather"]["history"])
    weather_forecast = pd.read_hdf(config.david["weather"]["h5file"],
                                   config.david["weather"]["forecast"])
    params = config.david["svm"]
    granularity = config.david["sampling"]["granularity"]
    fandata = pd.HDFStore(
        config.david["default"]["data_sources"] + "/lex560.h5").bms_hva_fan
    cleandata = fandata[fandata.FLOOR == 'F09'].drop_duplicates(
        subset="TIMESTAMP")

    # construct endogenous variable to run predictions on

    ts = pd.Series(data=list(cleandata.VALUE),
                   index=cleandata.TIMESTAMP)

    prediction = svm.model.predict(ts,
                                   weather_history,
                                   weather_forecast,
                                   params, granularity)
