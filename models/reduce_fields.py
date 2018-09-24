import copy
import time

from numpy import percentile

from models.raw_drain import hash_item


def check_ts(ts, start_ts, end_ts):
    if start_ts is not None:
        if start_ts > ts:
            return False
    if end_ts is not None:
        if end_ts < ts:
            return False
    return True


async def local_groups(start_ts, end_ts, fields: set, raw_dataset: dict):
    hashes = {}
    values = {}

    s1 = time.time()

    for ihash, item in raw_dataset["items"].items():

        if check_ts(item["time"], start_ts, end_ts):

            elapsed = raw_dataset["values"][ihash]

            h = hash_item(fields, item)

            if h not in hashes:
                hashes[h] = item
                values[h] = copy.copy(elapsed)
            else:
                for field in ('app_name', 'process', 'version', 'room', 'short_message', 'full_message', 'time'):
                    val = hashes.get(field)
                    if val not in (None, "mixed", item[field]):
                        hashes[h][field] = "mixed"
                values[h].extend(elapsed)

    s2 = time.time()
    print("s2", s2 - s1)

    processed_dataset = []
    for ihash, item in hashes.items():
        cval = values[ihash]
        percentiles = {
            "count": len(cval),
            "2_percentile": round(percentile(cval, 2), 3),
            "25_percentile": round(percentile(cval, 25), 3),
            "50_percentile": round(percentile(cval, 50), 3),
            "75_percentile": round(percentile(cval, 75), 3),
            "90_percentile": round(percentile(cval, 90), 3),
            "98_percentile": round(percentile(cval, 98), 3),
            "100_percentile": round(percentile(cval, 100), 3),
            "full_time": sum(cval),
            # percentile(raw_dataset[k], 25),
            # percentile(raw_dataset[k], 50),
            # percentile(raw_dataset[k], 75),
            # percentile(raw_dataset[k], 98),
        }
        processed_dataset.append((item, percentiles))
    s3 = time.time()
    print("s3", s3 - s2, s3 - s1)
    # pprint(processed_dataset)
    return processed_dataset


async def local_calc(hashes: dict, values: dict):
    processed = {}
    t1 = time.time()
    c = 0

    for ihash, item in hashes.items():
        cval = values[ihash]
        percentiles = {
            "count": len(cval),
            "2_percentile": round(percentile(cval, 2), 3),
            "25_percentile": round(percentile(cval, 25), 3),
            "50_percentile": round(percentile(cval, 50), 3),
            "75_percentile": round(percentile(cval, 75), 3),
            "90_percentile": round(percentile(cval, 90), 3),
            "98_percentile": round(percentile(cval, 98), 3),
            "100_percentile": round(percentile(cval, 100), 3),
            "full_time": sum(cval),
        }
        processed[ihash] = percentiles
        c += 1

    t2 = time.time()
    print("processed {} {:.3f}".format(c, t2 - t1))
    return processed


async def time_filter(start_ts, end_ts, hashes, values: dict):
    s1 = time.time()
    processed = []
    cc = 0
    for ihash, item in hashes.items():
        if check_ts(item["time"], start_ts, end_ts):
            cval = values[ihash]
            processed.append((item, cval))
            cc += 1
    s2 = time.time()
    print("s3", s2 - s1, cc)
    return processed
