import requests
import pandas as pd
import json
with open("../../config.json", "r") as fr:
    config = json.load(fr)
host = "api.bmreports.com"
port = "443"
version = "v1"


def getData(report="B1620", date="2019-03-14", save=False):
    URL = "https://%s:%s/BMRS/%s/%s" % (host, port, report, version)
    params = {"APIKey": config['elexonapikey'], "SettlementDate": date,
              "Period": "*", "ServiceType": "csv"}
    res = requests.get(URL, params=params)
    if res.status_code != 200:
        raise ValueError("Wrong status code %d" % res.status_code)
    if save:
        with open("%s_%s.csv" % (report, date), "w") as fw:
            fw.write(res.text)
    return res


if __name__ == '__main__':

    dates = pd.date_range(start="2015-01-01", end="2017-12-31")
    for d in dates:
        print("Processing %s" % d.strftime("%Y-%m-%d"))
        res = getData(date=d.strftime("%Y-%m-%d"), save=True)
