import aiohttp_jinja2
from aiohttp import web


class Main(web.View):
    async def get(self):
        context = {}
        response = aiohttp_jinja2.render_template('index.html',
                                                  self.request,
                                                  context)
        response.headers['Content-Language'] = 'ru'
        return response
