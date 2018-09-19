import datetime
import ujson as json

from aiohttp import web

from models.calculate import groups
from models.schemas import MyNormalizer, filter_schema


def expires_header():
    return datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")


def check_ts(ts, start_ts, end_ts):
    if start_ts is not None:
        if start_ts > ts:
            return False
    if end_ts is not None:
        if end_ts < ts:
            return False
    return True


class Reduce(web.View):
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

        processed = await groups(start_ts, end_ts, fields, self.request.app)

        response = {"code": 0, "response": processed}
        rsp = web.Response(content_type='application/json', text=json.dumps(response))
        # rsp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        # rsp.headers["Expires"] = expires_header()
        return rsp
