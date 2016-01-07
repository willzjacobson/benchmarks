# coding=utf-8

# import buildings_dbs as dbs
from numpy import logspace

import svm.model
from config import config
from ts_proc.utils import get_parsed_ts_new_schema
from weather.mongo import get_history, get_forecast

##########
dbs = config["building_dbs"]
buildings = config["default"]["buildings"]

for building in buildings:
    endog = get_parsed_ts_new_schema(host=dbs["mongo_cred"]["host"],
                                     port=dbs["mongo_cred"]["port"],
                                     database=dbs["building_ts_loc"][
                                         "db_name"],
                                     username=dbs["mongo_cred"][
                                         "username"],
                                     password=dbs["mongo_cred"]["password"],
                                     source=dbs["mongo_cred"]["source"],
                                     collection_name=dbs["building_ts_loc"][
                                         "collection_name"],
                                     building=building,
                                     device="Occupancy",
                                     system="Occupancy",
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

    cov = config["weather"]["cov"]
    gran = config["sampling"]["granularity"]
    params = config["svm"]["params"]
    pg = config["svm"]["param_search"]["grid"]
    param_grid = {"C": logspace(**(pg["C"])),
                  "gamma": logspace(**(pg["gamma"])),
                  "kernel": pg["kernel"]}
    cv = config["svm"]["param_search"]["cv"]
    n_jobs = config["svm"]["param_search"]["n_jobs"]
    threshold = config["svm"]["param_search"]["threshold"]
    has_bin_search = config["svm"]["param_search"]["has_bin_search"]
    discrete = True

    svm.model.predict(endog, weather_history, weather_forecast,
                      cov, gran, params, param_grid, cv, threshold,
                      n_jobs, discrete, has_bin_search)
