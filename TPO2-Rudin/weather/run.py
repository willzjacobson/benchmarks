import weather.helpers
import config

if __name__ == "__main__":
    city = config.david["weather"]["city"]
    state = config.david["weather"]["state"]
    archive_location = config.david["weather"]["h5file"]
    df_history = config.david["weather"]["history"]
    df_forecast = config.david["weather"]["forecast"]
    df_today_history = config.david["weather"]["today_history"]
    cap = config.david["weather"]["cap"]

    weather_history = weather.helpers.archive_update(city,
                                                     state,
                                                     archive_location,
                                                     df_history,
                                                     cap)
    latest_forecast = weather.helpers.forecast_munged(city, state)
    today_history = weather.helpers.history_munged()
    # weather_history.to_hdf(archive_location, df_history)
    latest_forecast.to_hdf(archive_location, df_forecast)
    today_history.to_hdf(archive_location, df_today_history)
