import weather

city = "New_York"
state = "NY"

weather_history = weather.archive_update(city, state)
latest_forecast = weather.forecast(city, state)

weather_history.to_hdf(
    'data/weather_history.h5', 'df_munged_resampled')

latest_forecast.to_hdf("data/weather_history.h5", 'forecast')
