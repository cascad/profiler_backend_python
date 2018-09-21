import time


def hash_item(fields, item: dict):
    return "*".join([str(item[i]) for i in fields])
    # return hash(item)


async def raw_drain(collection):
    hashes = {}
    values = {}
    t1 = time.time()
    fields = ('app_name', 'process', 'version', 'room', 'short_message', 'full_message', 'time')
    c = 0
    async with collection.find({},
                               {"_id": 0}).batch_size(10000) as cursor:  # .limit(100000)
        # .limit(50) # .batch_size(10).sort([('time', pymongo.DESCENDING)])
        async for item in cursor:
            elapsed = item["elapsed"]

            h = hash_item(fields, item)

            if h not in hashes:
                hashes[h] = item
                values[h] = [elapsed, ]
            else:
                values[h].append(elapsed)
            c += 1
    t2 = time.time()
    print("drained {} -> reduced {}: {:.3f}".format(c, len(hashes), t2 - t1))
    return hashes, values
