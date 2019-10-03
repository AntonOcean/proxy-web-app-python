import asyncio
import logging

from aiohttp import web

import settings
from db import setup_mongo
from routes import setup_routes, setup_routes_proxy


async def init_app_proxy():
    app = web.Application()

    setup_routes_proxy(app)
    return app


async def init_app(conf=settings.get_config()):
    app = web.Application()

    mongo = await setup_mongo(app, conf)
    app['mongo'] = mongo

    setup_routes(app)
    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    conf = settings.get_config()

    loop = asyncio.get_event_loop()
    # app = loop.run_until_complete(init_app(conf))
    # web.run_app(app, host=conf['host'], port=conf['port'])

    app = loop.run_until_complete(init_app_proxy())
    web.run_app(app, host=conf['host'], port=conf['proxy-port'])


if __name__ == '__main__':
    main()
