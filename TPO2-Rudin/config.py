david = {
    "default": {
        "base_dir": "/home/davidkarapetyan/Documents/workspace/Adirondack/analytics",
        "python_prog": "/home/davidkarapetyan/anaconda3/bin/python",
        "data_sources": "/data",
        "log_dir": "/var/log"
    },
    "weather": {
        "h5file": "/data/weather.h5",
        "wund_url": "http://api.wunderground.com/api/08d25f404214f50b/",
        # "wund_url": "http://api.wunderground.com/api/bab4ba5bcbc2dbec/",
        "cov": ["conds", "hum", "rain", "snow", "temp", "tornado", "thunder"],
        "today_history": "today_history",
        "history": "history",
        "forecast": "forecast",
        "city": "New_York",
        "state": "NY",
        "cap": 9
    },
    "sampling": {
        "granularity": "15min",
        "forecast_length": 24,
        "nary_thresh": 100
        # upper bound for number of unique points before time
        # series is classed as n-ary instead of continuous
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

ashish = {

    'default': {
        "base_dir": "/home/ashishgagneja/Adirondack/analytics/TPO2-Rudin",
        "python_prog": "/home/davidkarapetyan/anaconda3/bin/python",
        "data_sources": "/data",
        "log_dir": "/var/log"
    },

    'weather': {
        "wund_url": "http://api.wunderground.com/api/bab4ba5bcbc2dbec/",
        "table": "/data/weather.h5",
        "history": "history",
        "forecast": "forecast",
        "city": "New_York",
        "state": "NY",
        "cap": 9
    },

    'sampling': {
        "granularity": 15,
        "forecast_length": 24,
        "nary_thresh": 100,
        # upper bound for number of unique points before time
        # series is classed as n-ary instead of continuous
        "max_gap": 2,
        # largest allowed gap in data in hours
    },

    'svm': {
        "gamma": 1,
        "C": 1,
        "cache_size": 10000,
        "kernel": "rbf",
        "max_iter": -1,
        "probability": "False",
        "random_state": "None",
        "shrinking": "True",
        "tol": "0.001",
        "verbose": "False"
    },

    'sarima': {
        "order": "(1, 1, 0)",
        "seasonal_order": "(1,1,3)",
        "enforce_stationarity": "False"
    },

    'park345': {
        'steam_data': '/home/davidkarapetyan/data_analysis/data/park345.h5',
        'steam_data_group': 'oa_temp',
    }
}

master = None
