# coding=utf-8
# import pandas as pd
import larkin.weather.mongo
from __init__ import config

cfg = config["building_dbs"]
if __name__ == "__main__":
    dbs = config["building_dbs"]
    # whist = pd.read_hdf("/data/weather.h5", "history_orig")
    # weather.mongo._mongo_history_push(whist, **(cfg["mongo_cred"]),
    #                                   **(cfg["weather_history_loc"]))

    # bobo = weather.mongo.get_history(**(cfg["mongo_cred"]),
    #                              **(cfg["weather_history_loc"]))
    # hello = "string"
    larkin.weather.mongo.history_update(
            cap=90000000000,
            parallel=True,
            wund_url=dbs["wund_cred"]["wund_url"],
            city=dbs["wund_cred"]["city"],
            state=dbs["wund_url"]["state"],
            host=dbs["mongo_cred"]["host"],
            port=dbs["mongo_cred"]["port"],
            source=dbs["mongo_cred"]["source"],
            username=dbs["mongo_cred"][
                "username"],
            password=dbs["mongo_cred"]["password"],
            db_name=dbs["weather_history_loc"][
                "db_name"],
            collection_name=dbs["weather_history_loc"][
                "history"]
    )

    larkin.weather.mongo.forecast_update(
            wund_url=dbs["wund_cred"]["wund_url"],
            city=dbs["wund_cred"]["city"],
            state=dbs["wund_url"]["state"],
            host=dbs["mongo_cred"]["host"],
            port=dbs["mongo_cred"]["port"],
            source=dbs["mongo_cred"]["source"],
            username=dbs["mongo_cred"][
                "username"],
            password=dbs["mongo_cred"]["password"],
            db_name=dbs["weather_forecast_loc"][
                "db_name"],
            collection_name=dbs["weather_forecast_loc"][
                "history"])
