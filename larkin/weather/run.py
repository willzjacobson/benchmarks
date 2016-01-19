# coding=utf-8
# import pandas as pd
import larkin.weather.mongo
from larkin.user_config import user_config


def main():
    dbs = user_config["building_dbs"]
    larkin.weather.mongo.history_update(
            cap=90000000000,
            parallel=True,
            wund_url=dbs["wund_cred"]["wund_url"],
            city=dbs["wund_cred"]["city"],
            state=dbs["wund_cred"]["state"],
            host=dbs["mongo_cred"]["host"],
            port=dbs["mongo_cred"]["port"],
            source=dbs["mongo_cred"]["source"],
            username=dbs["mongo_cred"][
                "username"],
            password=dbs["mongo_cred"]["password"],
            db_name=dbs["weather_history_loc"][
                "db_name"],
            collection_name=dbs["weather_history_loc"][
                "collection_name"]
    )

    larkin.weather.mongo.forecast_update(
            wund_url=dbs["wund_cred"]["wund_url"],
            city=dbs["wund_cred"]["city"],
            state=dbs["wund_cred"]["state"],
            host=dbs["mongo_cred"]["host"],
            port=dbs["mongo_cred"]["port"],
            source=dbs["mongo_cred"]["source"],
            username=dbs["mongo_cred"][
                "username"],
            password=dbs["mongo_cred"]["password"],
            db_name=dbs["weather_forecast_loc"][
                "db_name"],
            collection_name=dbs["weather_forecast_loc"][
                "collection_name"])

    if __name__ == "__main__":
        main()
