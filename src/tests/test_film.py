from loguru import logger

import pytest


@pytest.mark.asyncio
async def test_service_is_up(redis, elastic):
    logger.info('start test services')
    es = await elastic.cluster.health()
    assert es['status'] == 'green'
    assert await redis.ping() == b'PONG'
    logger.info('end test services')
