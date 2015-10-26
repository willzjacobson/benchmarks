import weather

if __name__ == "__main__":
    city = "New_York"
    state = "NY"
    archive_location = "/data/weather.h5"
    df_history = "history"
    df_forecast = "forecast"
    cap = 9

    weather_history = weather.archive_update(city, state, archive_location,
                                             df_history,
                                             cap)
    latest_forecast = weather.forecast(city, state)
    weather_history.to_hdf(archive_location, df_history)
    latest_forecast.to_hdf(archive_location, df_forecast)
