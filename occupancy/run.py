# coding=utf-8

# import buildings_dbs as dbs
import svm.model
from config import config
from occupancy.svm_dframe_prep import get_covars
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

    covars = get_covars(endog=endog,
                        host=dbs["mongo_cred"]["host"],
                        port=dbs["mongo_cred"]["port"],
                        source=dbs["mongo_cred"]["source"],
                        username=dbs["mongo_cred"][
                            "username"],
                        password=dbs["mongo_cred"]["password"],
                        db_name=dbs["weather_history_loc"][
                            "db_name"],
                        collection_name=dbs["weather_history_loc"][
                            "collection_name"],
                        cov=config["weather"]["cov"],
                        gran=config["sampling"][
                            "granularity"]
                        )

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
