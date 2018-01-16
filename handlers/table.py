import datetime
import ujson as json

from aiohttp import web


def expires_header():
    return datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")


class Table(web.View):
    async def get(self):
        # data = await self.request.json()
        dataset = self.request.app.dataset
        response = {"code": 0, "response": dataset}
        rsp = web.Response(content_type='application/json', text=json.dumps(response))
        rsp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        rsp.headers["Expires"] = expires_header()
        return rsp
