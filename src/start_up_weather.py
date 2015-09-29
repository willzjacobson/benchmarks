import weather
city = "New_York"
state = "NY"

weather = weather.archive_update(city, state)
latest_forecast = weather.forecast(city, state)

weather.to_hdf("data/weather.h5", "history")
latest_forecast.to_hdf("data/weather.h5", "forecast")
