import asyncio
import inspect
import sys
import time
import traceback
import ujson as json
from pprint import pprint

from numpy import percentile

from models.raw_drain import raw_drain
from models.reduce_fields import local_calc
from settings import DATASET_COLLECTION, PROCESSOR_INTERVAL, DEBUG


async def drain_processor(app):
    now = time.time()
    app.proc_update_ts = now
    t1 = time.time()

    while True:
        try:
            hashes, values = await raw_drain(app.db.get_collection(DATASET_COLLECTION))
            app["raw_dataset"] = {"values": values, "items": hashes}
            app["percentiles"] = await local_calc(hashes, values)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback, limit=5)
            msg = {"exc_type": str(exc_type), "exc_value": str(exc_value), "exc_traceback": trace,
                   "ref": inspect.stack()[0][3]}
            print("{} Calculate error:\n".format(time.ctime()))
            pprint(msg)
            app.logger.error(str(msg))
        else:
            t2 = time.time()
            print("loaded {} -> {:.3f}: ".format(time.ctime(), t2-t1))

        now = time.time()
        sleep_time = PROCESSOR_INTERVAL
        app.proc_update_ts = now + sleep_time
        await asyncio.sleep(sleep_time)


async def groups(start_ts, end_ts, fields: set, app):
    coll = app.db.get_collection(DATASET_COLLECTION)
    hashes = {}
    raw_dataset = {}

    find_filter = {}

    if start_ts is not None:
        if find_filter.get("time") is None:
            find_filter["time"] = {}
        find_filter["time"]["$gte"] = start_ts
    if end_ts is not None:
        if find_filter.get("time") is None:
            find_filter["time"] = {}
        find_filter["time"]["$lte"] = end_ts
    print(find_filter)

    s1 = time.time()

    async with coll.find(find_filter,
                         {"_id": 0}).batch_size(3000) as cursor:  # .limit(50) # .sort([('time', pymongo.DESCENDING)])
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
                "full_message": item["full_message"],
                "time": item["time"]
            }
            hashable = {}

            for field in fields:
                hashable[field] = clean[field]

            h = json.dumps(hashable, sort_keys=True)

            if h not in hashes:
                hashes[h] = clean

                # hashes[h]["time"] = str(item["time"].timestamp())
                raw_dataset[h] = [elapsed, ]
            else:
                for field in ('app_name', 'process', 'version', 'room', 'short_message', 'full_message', 'time'):
                    val = hashes[h].get(field)
                    if val not in (None, "mixed", clean[field]):
                        hashes[h][field] = "mixed"

                raw_dataset[h].append(elapsed)

    s2 = time.time()
    print("s2", s2 - s1)

    processed_dataset = []
    for k, v in raw_dataset.items():
        percentiles = {
            "count": len(raw_dataset[k]),
            "2_percentile": round(percentile(raw_dataset[k], 2), 3),
            "25_percentile": round(percentile(raw_dataset[k], 25), 3),
            "50_percentile": round(percentile(raw_dataset[k], 50), 3),
            "75_percentile": round(percentile(raw_dataset[k], 75), 3),
            "90_percentile": round(percentile(raw_dataset[k], 90), 3),
            "98_percentile": round(percentile(raw_dataset[k], 98), 3),
            "100_percentile": round(percentile(raw_dataset[k], 100), 3),
            "full_time": sum(raw_dataset[k]),
            # percentile(raw_dataset[k], 25),
            # percentile(raw_dataset[k], 50),
            # percentile(raw_dataset[k], 75),
            # percentile(raw_dataset[k], 98),
        }
        processed_dataset.append((hashes[k], percentiles))
    s3 = time.time()
    print("s3", s3 - s2, s3 - s1)
    # pprint(processed_dataset)
    return processed_dataset


async def calc(filter: dict, app):
    coll = app.db.get_collection(DATASET_COLLECTION)
    hashes = {}
    raw_dataset = {}

    async with coll.find(filter,
                         {"_id": 0}).batch_size(3000) as cursor:
        # .limit(50) # .batch_size(10).sort([('time', pymongo.DESCENDING)])
        async for item in cursor:
            # ============================================================= Debug
            # if DEBUG:
            #     ff = False
            #     for i in ("elapsed", "app_name", "process", "version", "room", "short_message", "full_message"):
            #         if i not in item:
            #             ff = True
            #             break
            #     if ff:
            #         continue
            # ============================================================= End Debug

            elapsed = item["elapsed"]
            # clean = {
            #     "app_name": item["app_name"],
            #     "process": item["process"],
            #     "version": item["version"],
            #     "room": item["room"],
            #     "short_message": item["short_message"],
            #     "full_message": item["full_message"],
            #     "time": item["time"]
            # }

            hashable = {}

            for field in item.keys():
                hashable[field] = item

            h = json.dumps(hashable, sort_keys=True)

            # h = hash(str(clean))

            if h not in hashes:
                hashes[h] = item
                # hashes[h]["time"] = item["time"]
                raw_dataset[h] = [elapsed, ]
            else:
                raw_dataset[h].append(elapsed)
    processed_dataset = []

    for k, v in raw_dataset.items():
        percentiles = {
            "count": len(raw_dataset[k]),
            "2_percentile": round(percentile(raw_dataset[k], 2), 3),
            "25_percentile": round(percentile(raw_dataset[k], 25), 3),
            "50_percentile": round(percentile(raw_dataset[k], 50), 3),
            "75_percentile": round(percentile(raw_dataset[k], 75), 3),
            "90_percentile": round(percentile(raw_dataset[k], 90), 3),
            "98_percentile": round(percentile(raw_dataset[k], 98), 3),
            "100_percentile": round(percentile(raw_dataset[k], 100), 3),
            "full_time": sum(raw_dataset[k]),
            # percentile(raw_dataset[k], 25),
            # percentile(raw_dataset[k], 50),
            # percentile(raw_dataset[k], 75),
            # percentile(raw_dataset[k], 98),
        }
        # processed_dataset[json.dumps(hashes[k])] = percentiles
        processed_dataset.append((hashes[k], percentiles))

    # pprint(processed_dataset)
    return processed_dataset
