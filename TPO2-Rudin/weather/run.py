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

    weather.mongo.history_update(
            city=city, state=state, cap=cap, parallel=True,
            **(cfg["weather"]["mongo"]["history"])
    )

    weather.mongo.forecast_update(
            city=city, state=state, account=account,
            **(cfg["weather"]["mongo"]["forecast"]))


