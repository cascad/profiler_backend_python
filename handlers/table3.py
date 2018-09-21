import datetime
import time
import ujson as json

from aiohttp import web

from models.reduce_fields import local_calc
from models.schemas import MyNormalizer, table_schema


def expires_header():
    return datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")


def check_ts(ts, start_ts, end_ts):
    if start_ts is not None:
        if start_ts >= ts:
            return False
    if end_ts is not None:
        if end_ts <= ts:
            return False
    return True


def chunk_generator(data: list):
    for pack in data:
        yield json.dumps(pack)


class Table3(web.View):
    async def post(self):
        raw = await self.request.json()

        v = MyNormalizer(table_schema)
        validated = v.validate(raw)

        if not validated:
            response = {"code": 5, "response": v.errors}
            return web.Response(content_type='application/json', text=json.dumps(response))

        data = v.normalized(raw)

        start_ts = data.get("start_ts")
        end_ts = data.get("end_ts")

        raw_dataset = self.request.app["raw_dataset"]

        if not raw_dataset:
            response = {"code": 2, "response": "primary data processing is not complete"}
            return web.Response(content_type='application/json', text=json.dumps(response))

        items = raw_dataset["items"]
        values = self.request.app["percentiles"]

        s1 = time.time()
        result_dataset = []
        cc = 0
        for ihash, item in items.items():
            if check_ts(item["time"], start_ts, end_ts):
                cval = values[ihash]
                result_dataset.append((item, cval))
                cc += 1
        s2 = time.time()
        print("s3", s2 - s1, cc)

        response = {"code": 0, "response": result_dataset}
        # rsp = web.StreamResponse()
        # rsp.enable_chunked_encoding()
        # await rsp.prepare(self.request)
        rsp = web.Response(content_type='application/octet-stream', body=json.dumps(response))
        # rsp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        # rsp.headers["Expires"] = expires_header()
        return rsp
