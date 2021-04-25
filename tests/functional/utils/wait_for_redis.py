import logging
import os
import sys

import backoff

from redis import Redis
from redis.exceptions import ConnectionError as RedisConnectionError

# this need to add script start dir to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from core.config import cnf

logging.getLogger('backoff').addHandler(logging.StreamHandler())


class IsRedisReady:
    def __init__(self):
        self.redis = Redis(
            host=cnf.REDIS_HOST,
            port=cnf.REDIS_PORT,
            password=cnf.REDIS_PASSWORD,
            decode_responses=True,
        )

    @backoff.on_predicate(backoff.fibo, max_value=10)
    @backoff.on_exception(backoff.expo, RedisConnectionError)
    def ping(self) -> bool:
        if self.redis.ping():
            return True
        return False


IsRedisReady().ping()
