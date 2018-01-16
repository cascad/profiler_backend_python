import pymongo
from numpy import percentile

from lib.base import Mdict
from lib.country_codes import COUNTRY

author = 'warior'
date = '21.09.17'


ping = Mdict()
conn = pymongo.MongoClient("mongodb://192.168.1.140")
db = conn["perfomance"]
coll = db["rustz"]
data = coll.find({"category": "ping"})
for i in data:
    ping[i["geoip_country"]].append(i["value"])
print("Country, rate, ping[50per, 90per, 91per, 92per, 93per, 94per, 95per, 96per, 97per, 98per, 99per]")
country = ["RU", "US", "FR", "DE", "GB", "KR", "CA", "AU", "BR", "MX", "TH", "ES", "IT", "TW"]
for j in ping:
    if j in country:
        print("{0}, ping [{1}, {2}, {3}, {4}, {5}, "
              "{6}, {7}, {8}, {9}, {10}, {11}]".format(COUNTRY.get(j),
                                                       round(percentile(ping[j], 50), 0),
                                                       round(percentile(ping[j], 90), 0),
                                                       round(percentile(ping[j], 91), 0),
                                                       round(percentile(ping[j], 92), 0),
                                                       round(percentile(ping[j], 93), 0),
                                                       round(percentile(ping[j], 94), 0),
                                                       round(percentile(ping[j], 95), 0),
                                                       round(percentile(ping[j], 96), 0),
                                                       round(percentile(ping[j], 97), 0),
                                                       round(percentile(ping[j], 98), 0),
                                                       round(percentile(ping[j], 99), 0),
                                                       ))