from weather.helpers import forecast, archive_update
import config

if __name__ == "__main__":
    city = config.david.weather.city
    state = config.david.weather.state
    archive_location = config.david.data_sources + "/weather.h5"
    df_history = config.david.weather.history
    df_forecast = config.david.weather.forecast
    cap = config.david.weather.cap

    weather_history = archive_update(city,
                                     state,
                                     archive_location,
                                     df_history,
                                     cap)
    latest_forecast = forecast(city, state)
    weather_history.to_hdf(archive_location, df_history)
    latest_forecast.to_hdf(archive_location, df_forecast)
