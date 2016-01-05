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
                             password=dbs["mongo_cred"]["password"],
                             db_name=dbs["building_ts_loc"][
                                 "db_name"],
                             collection_name=dbs["building_ts_loc"][
                                 "collection_name"],
                             building=building)

    covars = get_covars(endog=endog,
                        host=dbs["mongo_cred"]["host"],
                        port=dbs["mongo_cred"]["port"],
                        source=dbs["mongo_cred"]["source"],
                        username=dbs["mongo_cred"][
                            "username"],
                        password=dbs["mongo_cred"]["password"],
                        db_name=dbs["building_ts_loc"][
                            "db_name"],
                        collection_name=dbs["building_ts_loc"][
                            "collection_name"],
                        cov=config["weather"]["cov"],
                        gran=config.config["sampling"][
                            "granularity"]
                        )

    weather_history = get_history(host=dbs["mongo_cred"]["host"],
                                  port=dbs["mongo_cred"]["port"],
                                  source=dbs["mongo_cred"]["source"],
                                  username=dbs["mongo_cred"][
                                      "username"],
                                  password=dbs["mongo_cred"]["password"],
                                  db_name=dbs["weather_history_loc"]["db_name"],
                                  collection_name=dbs["weather_history_loc"][
                                      "collection_name"])

    weather_forecast = get_forecast(host=dbs["mongo_cred"]["host"],
                                    port=dbs["mongo_cred"]["port"],
                                    source=dbs["mongo_cred"]["source"],
                                    username=dbs["mongo_cred"][
                                        "username"],
                                    password=dbs["mongo_cred"]["password"],
                                    db_name=dbs["weather_forecast_loc"][
                                        "db_name"],
                                    collection_name=dbs["weather_forecast_loc"][
                                        "collection_name"])

    svm.model.predict(endog=endog,
                      weather_history=weather_history,
                      weather_forecast=weather_forecast,
                      cov=config["weather"]["cov"],
                      gran=config["sampling"][
                          "granularity"],
                      **(config["svm"]["param_search"])
                        ** (config["svm"]["params"]),
                      discrete=True
                      )
