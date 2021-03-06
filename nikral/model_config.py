# coding=utf-8
model_config = dict(
        sampling={
            'forecast_length': 24,
            'granularity': '15min',
            'nary_thresh': 5,
            'accuracy': '1min',
            'gap_threshold': 2},
        svm={
            'param_search': {
                'cv': 2,
                'grid': {
                    'C': {
                        'base': 10,
                        'num': 50,
                        'start': 1,
                        'stop': 5},
                    'gamma': {
                        'base': 10,
                        'num': 50,
                        'start': -5,
                        'stop': 1},
                    'kernel': ['rbf']},
                'has_bin_search': False,
                'n_jobs': -1,
                'threshold': 0.003},
            'params': {
                'cache_size': 30000,
                'max_iter': -1,
                'shrinking': True,
                'tol': 0.001,
                'verbose': False},
            'cont_scofunc': 'mean_absolute_error',  # 'r2'
            'disc_scofunc': 'accuracy'
        },
        weather={
            'conds_mapping': {
                'Clear': 0,
                'Cloudy': 16,
                'Fog': 9,
                'Haze': 3,
                'Heavy Rain': 8,
                'Heavy Snow': 14,
                'Light Freezing Rain': 15,
                'Light Rain': 6,
                'Light Snow': 11,
                'Mist': 13,
                'Mostly Cloudy': 4,
                'Overcast': 5,
                'Partly Cloudy': 2,
                'Rain': 7,
                'Scattered Clouds': 1,
                'Showers': 7,
                'Snow': 12,
                'Unknown': 10},
            'cov': ['wetbulb'],
            'seasons': {
                'fall': [9, 12],
                'spring': [3, 6],
                'summer': [6, 9],
                'winter': [12, 3]},
            'wdire_mapping': {
                'ENE': 6,
                'ESE': 12,
                'East': 15,
                'NE': 5,
                'NNE': 3,
                'NNW': 4,
                'NW': 16,
                'North': 1,
                'SE': 10,
                'SSE': 11,
                'SSW': 13,
                'SW': 8,
                'South': 14,
                'Variable': 0,
                'WNW': 9,
                'WSW': 7,
                'West': 2}},
        arima={
            'order': [1, 1, 0]}
)
