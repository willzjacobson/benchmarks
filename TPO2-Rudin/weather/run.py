import weather.helpers
import config
import multiprocessing
import pandas as pd

if __name__ == "__main__":
    # pool=None
    pool = multiprocessing.Pool(
        processes=config.david["parallel"]["processors"])
    city = config.david["weather"]["city"]
    state = config.david["weather"]["state"]
    archive_location = config.david["weather"]["h5file"]
    history_name = config.david["weather"]["history"]
    forecast_name = config.david["weather"]["forecast"]
    history_orig_name = config.david["weather"]["history_orig"]
    forecast_orig_name = config.david["weather"]["forecast_orig"]
    cap = config.david["weather"]["cap"]
    gran = config.david["sampling"]["granularity"]
    account = config.david["weather"]["wund_url"]

    whist_noresamp = weather.helpers.archive_update(city, state,
                                                    archive_location,
                                                    history_orig_name, cap,
                                                    pool)
    whist_resamp = weather.helpers._history_resample(whist_noresamp, gran)

    forecast_noresamp = weather.helpers._forecast_munge(
        weather.helpers._forecast_pull(city, state, account))
    forecast_resamp = weather.helpers.forecast_update(
        city, state, account)


    # store resampled and nonresampled data in database, for debugging
    store = pd.HDFStore(archive_location)
    store[forecast_name] = forecast_resamp
    store[forecast_orig_name] = forecast_noresamp

    store[history_name] = whist_resamp
    store[history_orig_name] = whist_noresamp
    store.close()
