# coding=utf-8

# import buildings_dbs as dbs
import svm.model
from config import config
from occupancy.svm_dframe_prep import get_covars
from ts_proc.utils import get_occupancy_ts
from weather.mongo import get_history, get_forecast

##########
dbs = config["building_dbs"]
buildings = config["default"]["buildings"]

for building in buildings:
    endog = get_occupancy_ts(host=dbs["mongo_cred"]["host"],
                             port=dbs["mongo_cred"]["port"],
                             source=dbs["mongo_cred"]["source"],
                             username=dbs["mongo_cred"][
                                 "username"],
                             db_name=dbs["building_ts_loc"][
                                 "db_name"],
                             collection_name=dbs["building_ts_loc"][
                                 "collection_name"],
                             building=)

    covars = get_covars(endog=endog,
                        gran=config.config["sampling"][
                            "granularity"],
                        **(dbs["mongo_cred"]),
                        **(dbs["wund_cred"]),
                        **(dbs["weather_forecast_loc"]),
                        **(dbs["weather_history_loc"]),
                        )

    weather_history = get_history(**(dbs["mongo_cred"]),
                                  **(dbs["weather_history_loc"]))

    weather_forecast = get_forecast(**(dbs["mongo_cred"]),
                                    **(dbs["weather_forecast_loc"]))

    cov = config.config["weather"]["cov"]

svm.model.predict(endog=endog,
                  weather_history=weather_history,
                  weather_forecast=weather_forecast,
                  cov=cov
                  )

svm.model.predict(**(config["predict"]))
