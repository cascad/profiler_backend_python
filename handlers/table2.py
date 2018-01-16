from aiohttp import web

from models.calculate import calc


class Table2(web.View):
    async def get(self):
        # data = await self.request.json()
        data = await calc(self.request.app)

        return web.Response(content_type='application/json', text="ok")
