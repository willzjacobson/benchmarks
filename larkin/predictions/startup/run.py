# coding=utf-8

from numpy import logspace

import larkin.svm.model
from larkin.model_config import model_config
from larkin.ts_proc.munge import is_discrete, gap_resamp
from larkin.ts_proc.utils import get_parsed_ts_new_schema
from larkin.user_config import user_config
from larkin.weather.mongo import get_history, get_forecast

dbs = user_config["building_dbs"]
buildings = user_config["default"]["buildings"]

nary_thresh = model_config["sampling"]["nary_thresh"]
cov = model_config["weather"]["cov"]
gran = model_config["sampling"]["granularity"]
accuracy = model_config["sampling"]["accuracy"]
gap_threshold = model_config["sampling"]["gap_threshold"]
params = model_config["svm"]["params"]
pg = model_config["svm"]["param_search"]["grid"]
param_grid = {"C": logspace(**(pg["C"])),
              "gamma": logspace(**(pg["gamma"])),
              "kernel": pg["kernel"]}
cv = model_config["svm"]["param_search"]["cv"]
n_jobs = model_config["svm"]["param_search"]["n_jobs"]
threshold = model_config["svm"]["param_search"]["threshold"]
has_bin_search = model_config["svm"]["param_search"]["has_bin_search"]


def main():
    predictions = {}
    for building in buildings:
        endog = get_parsed_ts_new_schema(host=dbs["mongo_cred"]["host"],
                                         port=dbs["mongo_cred"]["port"],
                                         db_name=dbs["building_ts_loc"][
                                             "db_name"],
                                         username=dbs["mongo_cred"][
                                             "username"],
                                         password=dbs["mongo_cred"]["password"],
                                         source=dbs["mongo_cred"]["source"],
                                         collection_name=dbs["building_ts_loc"][
                                             "collection_name"],
                                         building=building,
                                         devices="S4-SupplyFanStatus",
                                         systems="S4",
                                         )

        # TODO fix this issue in the database, or have a script run befo hardw
        # def basic_filt(x):
        #     if x == 0.65:
        #         return 1
        #     elif x > 0.65:
        #         return 2
        #     else:
        #         return 0

        def basic_filt(x):
            if x == "active":
                return 1
            elif x == "inactive":
                return 0
            else:
                return x

        endog = endog.apply(basic_filt)
        endog = gap_resamp(endog, nary_thresh, gap_threshold, accuracy, gran)

        weather_history = get_history(host=dbs["mongo_cred"]["host"],
                                      port=dbs["mongo_cred"]["port"],
                                      source=dbs["mongo_cred"]["source"],
                                      username=dbs["mongo_cred"][
                                          "username"],
                                      password=dbs["mongo_cred"]["password"],
                                      db_name=dbs["weather_history_loc"][
                                          "db_name"],
                                      collection_name=
                                      dbs["weather_history_loc"][
                                          "collection_name"])

        weather_forecast = get_forecast(host=dbs["mongo_cred"]["host"],
                                        port=dbs["mongo_cred"]["port"],
                                        source=dbs["mongo_cred"]["source"],
                                        username=dbs["mongo_cred"][
                                            "username"],
                                        password=dbs["mongo_cred"]["password"],
                                        db_name=dbs["weather_forecast_loc"][
                                            "db_name"],
                                        collection_name=
                                        dbs["weather_forecast_loc"][
                                            "collection_name"])

        discrete = is_discrete(endog, nary_thresh)
        predictions.update({building: larkin.svm.model.predict(endog,
                                                               weather_history,
                                                               weather_forecast,
                                                               cov, gran,
                                                               params,
                                                               param_grid, cv,
                                                               threshold,
                                                               n_jobs, discrete,
                                                               has_bin_search)})
    return predictions


if __name__ == '__main__':
    pds = main()
