from common.utils import get_dt_tseries

__author__ = 'ashishgagneja'

import db.connect as connect
import pandas as pd
import electric.utils
import weather.helpers
import datetime
import occupancy.utils
import itertools
import weather.wet_bulb
import common.utils
import scipy


def _filter_missing_weather_data(weather_df):
    """
    Filter rows with missing data like -9999's

    :param weather_df: pandas DataFrame

    :return: pandas DataFrame
    """

    bad_data = weather_df.where(weather_df < -998).any(axis=1)
    # print('bad_data: %s' % bad_data[bad_data == True])
    return weather_df.drop(bad_data[bad_data == True].index)


def _get_weather(h5file_name, history_name, forecast_name, gran):
    """

    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file
    :return:
    """

    with pd.HDFStore(h5file_name) as store:

        munged_history = weather.helpers.history_munge(store[history_name],
                                                       "%dmin" % gran)

        munged_forecast = weather.helpers.forecast_munge(store[forecast_name],
                                                         "%dmin" % gran)
                                                         # cov, "%dmin" % gran)


    # drop unnecessary columns
    # TODO: this should be done before munging for efficiency but couldn't make
    # it work
    munged_history = munged_history[['temp', 'dewpt', 'pressure']]
    munged_forecast = munged_forecast[['temp', 'dewpoint', 'mslp']]

    # rename forecast columns to match the corresponding historical columns
    munged_forecast = munged_forecast.rename(columns={'dewpoint': 'dewpt',
                                                      'mslp': 'pressure'})

    all_weather = pd.concat([munged_history, munged_forecast])
    return _filter_missing_weather_data(all_weather)



def _get_data_availability_dates(obs_ts, gran):
    """
    Find dates for which data is available. Dates for which < threshold % data
    is available are dropped.

    Assumption: Series has no NA's
    Assumption: Threshold is 85

    :param obs_ts: pandas Series
    :param gran: int
        sampling frequency of input data and forecast data
    :return: set of dates for which
    """

    ts_list = list(map(datetime.datetime.date, obs_ts.index))
    counts = [[key, len(list(grp))] for key, grp in itertools.groupby(ts_list)]

    thresh = 0.85 * 24 * 60 / gran
    return set([key for key, cnt in itertools.filterfalse(
        lambda x: x[1] < thresh, counts)])



def _get_wetbulb_ts(weather_df):
    return weather_df.apply(weather.wet_bulb.compute_bulb_helper, axis=1)



def find_lowest_electric_usage(date_scores, electric_ts, n):

    dates, sim_scores = zip(*date_scores)

    # total_usage = []
    min_usage = [dates[0], sys.maxint, None]
    for dt in enumerate(dates):
        score = sim_scores[i]
        if score:

            # compute day electric usage by integrating the curve
            # Assumption: Linear interpolation is a reasonable way to fill gaps
            day_elec_ts = common.utils.drop_series_ix_date(
                common.utils.get_dt_tseries(dt, electric_ts))
            res = scipy.integration.cumtrapz(day_elec_ts.data,
                                             day_elec_ts.index, initial=0)
            print(res)
            # total_usage.append((dt, res[-1]))

            if res[-1] < min_usage[1]:
                min_usage = [dt, res[-1], day_elec_ts]

    return min_usage[0], min_usage[2]



def _find_benchmark(base_dt, occ_ts, wetbulb_ts, electric_ts, gran):

    # get data availability
    elec_avlblty = _get_data_availability_dates(electric_ts, gran)
    occ_avlblty = _get_data_availability_dates(occ_ts, gran)
    data_avlblty = occ_avlblty.intersection(elec_avlblty)

    # get weather for base_dt
    base_dt_wetbulb = common.utils.get_dt_tseries(base_dt, wetbulb_ts)

    # find k closest weather days for which electric and occupancy data is
    # available
    sim_wetbulb_days = common.utils.find_similar_profile_days(base_dt_wetbulb,
                                                              wetbulb_ts,
                                                              20,
                                                              data_avlblty)
    print("sim days: %s" % str(sim_wetbulb_days))

    # compute occupancy similarity score for the k most similar weather days
    occ_scores = occupancy.utils.score_occ_similarity(base_dt, sim_wetbulb_days)

    # find the date with the lowest electric usage
    return find_lowest_electric_usage(occ_scores, electric_ts)



def process_building(building_id, db_server, db_name, collection_name,
                     meter_count, h5file_name, history_name, forecast_name,
                     granularity, base_dt):

    """ Find baseline electric usage for building_id

    :param building_id: string
        building_id identifier
    :param db_server: string
        database server name or IP-address
    :param db_name: string
        name of the database on server
    :param collection_name: string
        name of collection in the database
    :param meter_count: int
        number of electric meters
    :param h5file_name: string
        path to HDF5 file containing weather data
    :param history_name: string
        group identifier for historical weather data within the HDF5 file
    :param forecast_name: string
        group identifier for weather forecast within the HDF5 file
    :param granularity: int
        expected frequency of observations and forecast in minutes
    :param base_dt: datetime.date
        date for which benchmark electric usage is to be found
    :return:
    """

    # connect to database
    # conn = connect.connect(db_server, database=db_name)
    # db = conn[db_name]

    occ_ts = occupancy.utils.get_occupancy_ts(db_server, db_name,
                                              collection_name, building_id)
    print("occupancy: %s" % occ_ts)

    # query electric data
    elec_ts = electric.utils.get_electric_ts(db_server, db_name,
                                             collection_name, building_id,
                                             meter_count, granularity)
    print(elec_ts)

    # get weather data
    weather_df = _get_weather(h5file_name, history_name, forecast_name,
                              granularity)
    print("weather: %s" % weather_df)
    wetbulb_ts = _get_wetbulb_ts(weather_df)
    print("wetbulb: %s" % wetbulb_ts)



    # find baseline
    bench_dt, bench_usage = _find_benchmark(base_dt, occ_ts, wetbulb_ts,
                                            elec_ts, granularity)

    # TODO: save results
    conn.close()
