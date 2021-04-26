import asyncio
import json
import os
import sys
from pathlib import Path

import aiohttp

from multidict import CIMultiDictProxy

import pytest

import aioredis

from elasticsearch import AsyncElasticsearch

# this need to add script start dir to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from core.config import config

from db import elastic
from db import redis


TEST_JSON_PATH = 'tests/data/'


# https://github.com/pytest-dev/pytest-asyncio/issues/68
# https://github.com/pytest-dev/pytest-asyncio/issues/171
# https://github.com/pytest-dev/pytest-asyncio
@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def redis():
    redis.redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT),
        password=config.REDIS_PASSWORD,
        minsize=10, maxsize=20
    )
    yield redis.redis
    # await redis.redis.close()


@pytest.fixture(scope='session')
async def elastic():
    elastic.es = AsyncElasticsearch(
        hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'],
        scheme=config.ELASTIC_SCHEME,
        http_auth=(config.ELASTIC_USER, config.ELASTIC_PASSWORD)
    )
    yield elastic
    # await elastic.es.close()


# https://stackoverflow.com/questions/50329629/how-to-access-a-json-filetest-data-like-config-json-in-conftest-py
@pytest.fixture
async def read_json_data(request):
    async def inner(datafilename: str) -> dict:
        jsonpath = Path(Path.cwd(), TEST_JSON_PATH, datafilename)
        with jsonpath.open() as fp:
            data = json.load(fp)
        return data
    return inner
