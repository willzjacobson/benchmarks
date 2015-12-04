import pandas as pd

import config
import weather.helpers

if __name__ == "__main__":
    city = config.david["weather"]["city"]
    state = config.david["weather"]["state"]
    archive_location = config.david["weather"]["h5file"]
    cov = config.david["weather"]["cov"]
    history_munged_name = config.david["weather"]["history"]
    forecast_munged_name = config.david["weather"]["forecast"]
    history_orig_name = config.david["weather"]["history_orig"]
    forecast_orig_name = config.david["weather"]["forecast_orig"]
    cap = config.david["weather"]["cap"]
    gran = config.david["sampling"]["granularity"]
    account = config.david["weather"]["wund_url"]

    whist_orig = weather.helpers.history_update(city, state,
                                                archive_location,
                                                history_orig_name, cap,
                                                parallel=True,
                                                munged=False)
    whist_munged = weather.helpers.history_update(city, state,
                                                  archive_location,
                                                  history_munged_name, cap,
                                                  parallel=True,
                                                  gran=gran,
                                                  munged=True)

    forecast_orig = weather.helpers.forecast_update(city, state, account,
                                                    munged=False)
    forecast_munged = weather.helpers.forecast_update(city, state, account,
                                                      gran=gran,
                                                      munged=True)
    # store munged and pure data in database, for debugging
    store = pd.HDFStore(archive_location)
    store[forecast_munged_name] = forecast_munged
    store[forecast_orig_name] = forecast_orig

    store[history_munged_name] = whist_munged
    store[history_orig_name] = whist_orig
    store.close()
