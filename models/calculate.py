import asyncio
import inspect
import sys
import time
import traceback
import ujson as json
from pprint import pprint

import pymongo
from numpy import percentile

from settings import DATASET_COLLECTION, PROCESSOR_INTERVAL, DEBUG


async def processor(app):
    now = time.time()
    app.proc_update_ts = now

    while True:
        try:
            app.dataset = await calc(app)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback, limit=5)
            msg = {"exc_type": str(exc_type), "exc_value": str(exc_value), "exc_traceback": trace,
                   "ref": inspect.stack()[0][3]}
            print("{} Calculate error:\n".format(time.ctime()))
            pprint(msg)
            app.logger.error(str(msg))
        else:
            print("loaded -> {}".format(time.ctime()))

        now = time.time()
        sleep_time = PROCESSOR_INTERVAL
        app.proc_update_ts = now + sleep_time
        await asyncio.sleep(sleep_time)


async def calc(app):
    coll = app.db.get_collection(DATASET_COLLECTION)
    hashes = {}
    raw_dataset = {}
    async with coll.find({}, {"_id": 0}) as cursor:  # .limit(50) # .batch_size(10).sort([('time', pymongo.DESCENDING)])
        async for item in cursor:

            # ============================================================= Debug
            if DEBUG:
                # print(item)
                ff = False
                for i in ("elapsed", "app_name", "process", "version", "room", "short_message", "full_message"):
                    if i not in item:
                        ff = True
                        break
                if ff:
                    continue
            # ============================================================= End Debug

            elapsed = item["elapsed"]
            clean = {
                "app_name": item["app_name"],
                "process": item["process"],
                "version": item["version"],
                "room": item["room"],
                "short_message": item["short_message"],
                "full_message": item["full_message"]
            }
            h = hash(str(clean))
            if h not in hashes:
                hashes[h] = clean
                hashes[h]["time"] = str(item["time"].date())
                raw_dataset[h] = [elapsed, ]
            else:
                raw_dataset[h].append(elapsed)
    # pprint(raw_dataset)

    processed_dataset = {}
    for k, v in raw_dataset.items():
        percentiles = {
            "count": len(raw_dataset[k]),
            "2_percentile": round(percentile(raw_dataset[k], 2), 3),
            "25_percentile": round(percentile(raw_dataset[k], 25), 3),
            "50_percentile": round(percentile(raw_dataset[k], 50), 3),
            "75_percentile": round(percentile(raw_dataset[k], 75), 3),
            "90_percentile": round(percentile(raw_dataset[k], 90), 3),
            "98_percentile": round(percentile(raw_dataset[k], 98), 3),
            "full_time": sum(raw_dataset[k]),
            # percentile(raw_dataset[k], 25),
            # percentile(raw_dataset[k], 50),
            # percentile(raw_dataset[k], 75),
            # percentile(raw_dataset[k], 98),
        }
        processed_dataset[json.dumps(hashes[k])] = percentiles
    # pprint(processed_dataset)
    return processed_dataset
