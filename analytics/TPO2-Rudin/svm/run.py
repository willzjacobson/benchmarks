__author__ = 'davidkarapetyan'

import svm
import config
import pandas as pd

if __name__ == "__main__":
    wdata = pd.HDFStore("/data/weather.h5")

    prediction = svm.model_predict(endog,
                                   wdata.archive,
                                   wdata.forecast,
                                   params=config.david["svm"])
