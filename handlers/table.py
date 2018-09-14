import datetime
import ujson as json

from aiohttp import web


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


class Table(web.View):
    async def post(self):
        data = await self.request.json()
        start_ts = data.get("start_ts")
        end_ts = data.get("end_ts")
        dataset = self.request.app.dataset
        result_dataset = {}

        for k, v in dataset.items():
            k_dict = json.loads(k)
            t = k_dict["time"]
            if check_ts(t, start_ts, end_ts):
                result_dataset[k] = v

        response = {"code": 0, "response": dataset}
        rsp = web.Response(content_type='application/json', text=json.dumps(response))
        # rsp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        # rsp.headers["Expires"] = expires_header()
        return rsp
