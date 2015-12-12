import pandas as pd

import config
import weather.mongo
import weather.wund

cfg = config.david
if __name__ == "__main__":
    city = cfg["weather"]["city"]
    state = cfg["weather"]["state"]
    archive_location = cfg["weather"]["h5file"]
    cov = cfg["weather"]["cov"]
    history_munged_name = cfg["weather"]["history"]
    forecast_munged_name = cfg["weather"]["forecast"]
    history_orig_name = cfg["weather"]["history_orig"]
    forecast_orig_name = cfg["weather"]["forecast_orig"]
    cap = cfg["weather"]["cap"]
    gran = cfg["sampling"]["granularity"]
    account = cfg["weather"]["wund_url"]

    # bobo = weather.utils.get_latest_forecast(gran="15min", munged=True,
    #                                           **(cfg["weather"]["mongo"][
    #                                                 "forecast"]))

    whist_orig = weather.mongo.mongo_history_update(
            city, state,
            archive_location,
            history_orig_name, cap,
            parallel=True,
            munged=False,
            **(cfg["weather"]["mongo"]["history"])
    )
    whist_munged = weather.mongo.mongo_history_update(
            city, state,
            archive_location,
            history_munged_name, cap,
            parallel=True,
            gran=gran,
            munged=True,
            **(cfg["weather"]["mongo"]["history"])
    )

    forecast_orig = weather.wund.forecast_update(
            city, state, account,
            munged=False,
            **(cfg["weather"]["mongo"]["forecast"]))
    forecast_munged = weather.wund.forecast_update(
            city, state, account,
            gran=gran,
            munged=True,
            **(cfg["weather"]["mongo"]["forecast"]))

    # store munged and pure data in database, for debugging
    store = pd.HDFStore(archive_location)
    store[forecast_munged_name] = forecast_munged
    store[forecast_orig_name] = forecast_orig

    store[history_munged_name] = whist_munged
    store[history_orig_name] = whist_orig
    store.close()
