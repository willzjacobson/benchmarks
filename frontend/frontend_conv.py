# coding=utf-8
import json

__author__ = 'davidkarapetyan'


def frontend_conv(ts):
    """Converts Pandas time series to format specified by frontend team

    :param ts: series object
    :return: dictionary
    """
    temp = json.loads(ts.to_json(date_format="iso", orient="split"))
    ts_list = [{"time": time, "value": value} for time, value in
               zip(temp["index"], temp['data'])]
    new_dict = {'time_series': ts_list, 'name': temp['name']}
    return new_dict
