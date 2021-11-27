import requests
import json
import time

import config


def load_json():
    resp = requests.get(config.URL_EX)

    with open("data.json", "w") as f:
        f.write(resp.text)


def load_exchange():

    with open("data.json") as json_file:
        data = json.load(json_file)
    timestamp = data["timestamp"]
    if (round(time.time(), 0) - timestamp) > 3000:
        load_json()
    rates = data["rates"]
    bdt = rates["BDT"]
    rub = rates["RUB"]
    curs = rub / bdt
    return round(curs, 2)


def time_update():
    with open("data.json") as json_file:
        data = json.load(json_file)
        timestamp = data["timestamp"]
        date = time.strftime("%H:%M:%S", time.localtime(timestamp))
    return date
