# coding=utf-8
import config
import weather.mongo
import weather.wund

cfg = config.david["building_dbs"]
if __name__ == "__main__":
    city = cfg["building_dbs"]["city"]
    state = cfg["building_dbs"]["state"]
    cov = cfg["building_dbs"]["cov"]
    cap = cfg["building_dbs"]["cap"]
    gran = cfg["sampling"]["granularity"]
    account = cfg["building_dbs"]["wund_url"]

    # whist = pd.read_hdf("/data/weather.h5", "history_orig")
    # weather.mongo_cred._mongo_history_push(
    # whist, **(cfg["weather"]["mongo_cred"]["history"]))

    weather.mongo.history_update(
            cap=90000000000,
            **(cfg["wund_cred"]),
            **(cfg["mongo_cred"]),
            **(cfg["mongo_cred"]["weather_history_loc"]))

    weather.mongo.forecast_update(
            **(cfg["wund_cred"]),
            **(cfg["mongo_cred"]),
            **(cfg["building_dbs"]["mongo_cred"]["weather_forecast_loc"]))
