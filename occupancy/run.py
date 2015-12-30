# coding=utf-8

import config
import svm
import ts_proc.utils
import weather.mongo
from occupancy.svm_dframe_prep import get_covars

dbs = config.david["building_dbs"]
for building in config.david['default']['buildings']:
    endog = ts_proc.utils.get_occupancy_ts(**(dbs["mongo_cred"]),
                                           **(dbs["weather_history_loc"]),
                                           **(dbs["building_ts_loc"]),
                                           )

    covars = get_covars(endog=endog,
                        gran=config.david["sampling"][
                            "granularity"],
                        **(dbs["mongo_cred"]),
                        **(dbs["wund_cred"]),
                        **(dbs["weather_forecast_loc"]),
                        **(dbs["weather_history_loc"]),
                        )

    weather_history = weather.mongo.get_history(**(dbs["mongo_cred"]),
                                                **(dbs["weather_history_loc"]))

    weather_forecast = weather.mongo.get_forecast(**(dbs["mongo_cred"]),
                                                  **(
                                                      dbs[
                                                          "weather_forecast_loc"]))

svm.predict(endog=endog, )
