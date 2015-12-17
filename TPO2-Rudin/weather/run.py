# coding=utf-8
import config
import weather.mongo
import weather.wund

cfg = config.david["building_dbs"]
if __name__ == "__main__":
    # whist = pd.read_hdf("/data/weather.h5", "history_orig")
    # weather.mongo_cred._mongo_history_push(
    # whist, **(cfg["weather"]["mongo_cred"]["history"]))

    weather.mongo.history_update(
            cap=90000000000,
            parallel=False,
            **(cfg["wund_cred"]),
            **(cfg["mongo_cred"]),
            **(cfg["weather_history_loc"]))

    weather.mongo.forecast_update(
            **(cfg["wund_cred"]),
            **(cfg["mongo_cred"]),
            **(cfg["weather_forecast_loc"]))
