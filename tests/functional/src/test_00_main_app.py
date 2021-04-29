from loguru import logger

import pytest


# Базовые проверки на то, что все сервисы отвечают
@pytest.mark.asyncio
async def test_film(make_get_request):
    logger.info('test for film api alive')
    response = await make_get_request('film')
    assert response.status == 200
    assert len(response.body) == 50
    logger.info('film api is alive')


@pytest.mark.asyncio
async def test_genres(make_get_request):
    logger.info('test for genre api alive')
    response = await make_get_request('genre')
    assert response.status == 200
    assert len(response.body) == 28
    logger.info('genre api is alive')


@pytest.mark.asyncio
async def test_persons(make_get_request):
    logger.info('test for person api alive')
    response = await make_get_request('person')
    assert response.status == 200
    assert len(response.body) == 50
    logger.info('person api is alive')
