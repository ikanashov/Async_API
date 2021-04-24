import pytest

# from loguru import logger


@pytest.mark.asyncio
async def test_film(make_get_request):
    # Выполнение запроса
    response = await make_get_request('film')

    # logger.debug('do response test')

    # Проверка результата
    assert response.status == 200
    # logger.info('pass response test')
    assert len(response.body) == 50
    # logger.info('response lenght is ok')
    # assert response.body == expected


@pytest.mark.asyncio
async def test_genres(make_get_request):
    # Выполнение запроса
    response = await make_get_request('genre')

    # logger.debug('do response test')

    # Проверка результата
    assert response.status == 200
    # logger.info('pass response test')
    assert len(response.body) == 28
    # logger.info('response lenght is ok')
    # assert response.body == expected


@pytest.mark.asyncio
async def test_persons(make_get_request):
    # Выполнение запроса
    response = await make_get_request('person')

    # logger.debug('do response test')

    # Проверка результата
    assert response.status == 200
    # logger.info('pass response test')
    assert len(response.body) == 50
    # logger.info('response lenght is ok')
    # assert response.body == expected
