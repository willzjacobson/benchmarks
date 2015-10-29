david = {
    "default": {
        "base_dir": "/home/davidkarapetyan/Documents/workspace/Adirondack/analytics",
        "python_prog": "/home/davidkarapetyan/anaconda3/bin/python",
        "data_sources": "/data",
        "log_dir": "/var/log"
    },
    "weather": {
        "h5file": "/data/weather.h5",
        "wund_url": "http://api.wunderground.com/api/bab4ba5bcbc2dbec/",
        "history": "history",
        "forecast": "forecast",
        "city": "New_York",
        "state": "NY",
        "cap": 9
    },
    "sampling": {
        "granularity": 15,  # units are minutes
        "forecast_length": 24
    },
    "svm": {
        "gamma": 1,
        "C": 1,
        "cache_size": 10000,
        "kernel": "rbf",
        "max_iter": -1,
        "probability": "False",
        "random_state": 1,
        "shrinking": "True",
        "tol": "0.001",
        "verbose": "False",
    },
    "sarima": {
        "order": "(1, 1, 0)",
        "seasonal_order": "(1,1,3)",
        "enforce_stationarity": "False"
    }}

ashish = None
master = None
