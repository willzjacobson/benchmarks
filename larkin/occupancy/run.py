# coding=utf-8

from numpy import logspace

from larkin.config import config
from larkin.ts_proc.munge import is_discrete
from larkin.weather.mongo import get_history, get_forecast
from ts_proc.utils import get_parsed_ts_new_schema

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

    nary_thresh = config["sampling"]["nary_thresh"]
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
    discrete = is_discrete(endog, nary_thresh)

    larkin.svm.model.predict(endog, weather_history, weather_forecast,
                             cov, gran, params, param_grid, cv, threshold,
                             n_jobs, discrete, has_bin_search)
