import asyncio
import logging

from aiohttp import web

import settings
from db import setup_mongo
from routes import setup_routes


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
    app = loop.run_until_complete(init_app(conf))
    web.run_app(app, host=conf['host'], port=conf['port'])


if __name__ == '__main__':
    main()
