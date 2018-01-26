#! /usr/bin/env python
import asyncio
import sys

import aiohttp_cors
import aiohttp_jinja2
import aiomongo
import jinja2
from aiohttp import web

import routes
from models.calculate import processor
from settings import *


async def shutdown(server, app, handler):
    server.close()
    await server.wait_closed()
    app.client.close()  # database connection close
    await app.shutdown()
    await handler.shutdown(10.0)
    await app.cleanup()


async def init(loop):
    # middle = [
    #     session_middleware(
    #         EncryptedCookieStorage(SECRET_KEY.encode("utf8"), cookie_name="KEFIR_WEB", httponly=False)),
    #     authorize,
    #     db_handler,
    # ]

    app = web.Application(loop=loop, )  # middlewares=middle

    # route part
    for route in routes.routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    # end route part

    if DEBUG:
        # Configure default CORS settings.
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        # Configure CORS on all routes.
        for route in list(app.router.routes()):
            cors.add(route)

    # Configure Jinja2
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATE_PATH))

    # Add static
    # if DEBUG:
    app.router.add_static('/', STATIC_PATH, name='static')

    # db connect
    client = app.client = await aiomongo.create_client('mongodb://' + MONGO_HOST,
                                                       loop=loop)
    app.db = client.get_database(MONGO_DB_NAME)
    # end db connect

    app.processor = asyncio.ensure_future(processor(app))
    app.dataset = None
    app.proc_update_ts = None

    handler = app.make_handler()
    serv_generator = loop.create_server(handler, HOST, PORT)
    return serv_generator, handler, app


if sys.platform == 'linux':
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

loop = asyncio.get_event_loop()

serv_generator, handler, app = loop.run_until_complete(init(loop))
serv = loop.run_until_complete(serv_generator)
log.debug('start server %s' % str(serv.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    log.debug(' Stop server begin')
finally:
    loop.run_until_complete(shutdown(serv, app, handler))
    loop.close()
log.debug('Stop server end')
