import logging
import os

import motor.motor_asyncio as aiomotor
from pymongo import errors

logger = logging.getLogger(__name__)


async def init_mongo(conf):
    host = os.environ.get('DOCKER_DB_LINK', conf['host'])
    mongo_uri = "mongodb://{}:{}".format(host, conf['port'])
    conn = aiomotor.AsyncIOMotorClient(
        mongo_uri,
        maxPoolSize=conf['max_pool_size']
    )
    db_name = conf['database']
    return conn[db_name]


async def setup_mongo(app, conf):
    mongo = await init_mongo(conf['mongo'])

    try:
        result = await mongo.command('ping')
        logger.log(level=logging.DEBUG, msg=f"Mongo: {result}")
    except errors.ServerSelectionTimeoutError:
        logger.log(level=logging.ERROR, msg="Fail connect to Mongo")

    async def close_mongo(app):
        mongo.client.close()

    app.on_cleanup.append(close_mongo)
    return mongo
