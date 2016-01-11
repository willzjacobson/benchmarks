# coding=utf-8
# import pandas as pd
import weather.mongo
import weather.wund
from config import config

cfg = config["building_dbs"]
if __name__ == "__main__":
    # whist = pd.read_hdf("/data/weather.h5", "history_orig")
    # weather.mongo._mongo_history_push(whist, **(cfg["mongo_cred"]),
    #                                   **(cfg["weather_history_loc"]))

    # bobo = weather.mongo.get_history(**(cfg["mongo_cred"]),
    #                              **(cfg["weather_history_loc"]))
    # hello = "string"
    weather.mongo.history_update(
            cap=90000000000,
            parallel=True,
            **(cfg["wund_cred"]),
            **(cfg["mongo_cred"]),
            **(cfg["weather_history_loc"]))

    weather.mongo.forecast_update(
            **(cfg["wund_cred"]),
            **(cfg["mongo_cred"]),
            **(cfg["weather_forecast_loc"]))
