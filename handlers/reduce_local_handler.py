import datetime
import ujson as json

from aiohttp import web

from models.reduce_fields import local_groups
from models.schemas import MyNormalizer, filter_schema


def expires_header():
    return datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")


def chunk_generator(data: list):
    for pack in data:
        yield json.dumps(pack)


class ReduceLocal(web.View):
    async def post(self):
        raw = await self.request.json()

        v = MyNormalizer(filter_schema)
        validated = v.validate(raw)

        if not validated:
            response = {"code": 5, "response": v.errors}
            return web.Response(content_type='application/json', text=json.dumps(response))

        data = v.normalized(raw)

        start_ts = data.get("start_ts")
        end_ts = data.get("end_ts")
        fields = set(data.get("fields", []))
        dataset = self.request.app["raw_dataset"]

        if not dataset:
            response = {"code": 2, "response": "primary data processing is not complete"}
            return web.Response(content_type='application/json', text=json.dumps(response))

        result = await local_groups(start_ts, end_ts, fields, dataset)

        response = {"code": 0, "response": result}
        # rsp = web.StreamResponse()
        # rsp.enable_chunked_encoding()
        # await rsp.prepare(self.request)
        rsp = web.Response(content_type='application/octet-stream', body=json.dumps(response))
        # rsp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        # rsp.headers["Expires"] = expires_header()
        return rsp
