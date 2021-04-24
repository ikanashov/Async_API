import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import json
from pathlib import Path

import asyncio
import aiohttp
import pytest

from dataclasses import dataclass
from multidict import CIMultiDictProxy

from loguru import logger

from core.config import cnf


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int

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
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(service: str, method: str = '', params: dict = None) -> HTTPResponse:
        params = params or {}
        url = cnf.NGINX_URL + cnf.API_URL + service + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
          return HTTPResponse(
            body=await response.json(),
            headers=response.headers,
            status=response.status,
          )
    return inner


# https://stackoverflow.com/questions/50329629/how-to-access-a-json-filetest-data-like-config-json-in-conftest-py
@pytest.fixture
async def read_json_data(request):
    async def inner(datafilename: str) -> dict:
        # logger.debug('read json data')
        jsonpath =  Path(Path.cwd(), cnf.TEST_JSON_PATH, datafilename)
        with jsonpath.open() as fp:
            data = json.load(fp)
        return data
    return inner
