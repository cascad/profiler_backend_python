import datetime
import time
import asyncio
from aiohttp import web
import ujson as json

from models.calculate import calc, processor


def expires_header():
    return datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")


class Status(web.View):
    async def get(self):
        app = self.request.app
        # data = await self.request.json()
        proc_status = not app.processor.done()
        if not proc_status:
            app.processor = asyncio.ensure_future(processor(app))
        next_update = time.ctime(app.proc_update_ts)
        response = {"code": 0 if proc_status else 1, "response": next_update}
        rsp = web.Response(content_type='application/json', text=json.dumps(response))
        rsp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        rsp.headers["Expires"] = expires_header()
        return rsp
