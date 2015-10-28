__author__ = 'davidkarapetyan'

import json


def frontend_conv(ts):
    temp = json.loads(ts.to_json(date_format="iso", orient="split"))
    filename = "/data/" + ts.name + ".json"

    ts_list = [{"time": time, "value": value} for time, value in
               zip(temp["index"], temp['data'])]
    new_json = {'time_series': ts_list, 'name': temp['name']}
    file = open(filename, "w")
    json.dump(new_json, file)
    file.close()
