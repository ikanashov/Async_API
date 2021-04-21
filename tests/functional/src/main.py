import asyncio
import aiohttp
import pytest

from dataclasses import dataclass
from multidict import CIMultiDictProxy

from loguru import logger

SERVICE_URL = 'http://SERVER_FOR_TEST:8088'


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
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + '/api/v1/film' + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
          return HTTPResponse(
            body=await response.json(),
            headers=response.headers,
            status=response.status,
          )
    return inner


@pytest.mark.asyncio
async def test_search_detailed(make_get_request):
    # Выполнение запроса
    response = await make_get_request('/search', {'query': 'Star Wars'})
    
    logger.debug('I am here')

    # Проверка результата
    assert response.status == 200
    assert len(response.body) == 50

    #assert response.body == expected