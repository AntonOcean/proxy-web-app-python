import logging
import os
import pathlib

import trafaret as t
import yaml

logger = logging.getLogger(__name__)

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG = 'config.yml'
CITIZENS_COLLECTION = 'requests_dump'

config_template = t.Dict({
    t.Key('mongo'): t.Dict({
        t.Key('host'): t.Regexp(regexp=r'^\d+.\d+.\d+.\d+$'),
        t.Key('port'): t.Int(gte=0),
        t.Key('database'): t.String(),
        t.Key('max_pool_size'): t.Int(gte=0),
    }),
    t.Key('host'): t.Regexp(regexp=r'^\d+.\d+.\d+.\d+$'),
    t.Key('port'): t.Int(gte=0),
})


def get_config(mode=DEFAULT_CONFIG):
    config_path = os.path.join(BASE_DIR, 'config', mode)

    with open(config_path, 'rt') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        try:
            config_template.check(config)
        except t.DataError:
            logger.log(level=logging.ERROR, msg="send bad config to App")
    return config
