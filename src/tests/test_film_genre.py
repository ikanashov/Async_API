from loguru import logger

import pytest

from models.film import SFilmGenre

from services import genre as genre_db


@pytest.fixture(scope='module')
async def genre(conf, datastore):
    logger.info('setup genre class')
    genre_db.datastore = datastore
    genre = genre_db.Genre()
    await genre.set_genre_index(conf.ELASTIC_GENRE_INDEX)
    yield genre
    logger.info('end setup genre class')


@pytest.mark.asyncio
async def test_film_Genre_Class(conf, genre: genre_db.Genre, cache, redis, read_json_data):
    logger.info('test film genre class')
    datas = await read_json_data('es_genres_data.json')
    for data in datas:
        await redis.delete(cache.genkey(index=conf.ELASTIC_GENRE_INDEX, id=data['id']))
        doc = await genre.get_genre_by_id(data['id'])
        cache_doc = await cache.get_data(index=conf.ELASTIC_GENRE_INDEX, id=data['id'])
        assert doc == SFilmGenre(**data)
        assert doc == SFilmGenre(**cache_doc)
    logger.info('end test film genre class')


@pytest.mark.asyncio
async def test_film_get_all_genre_Genre_Class(genre: genre_db.Genre, read_json_data):
    logger.info('test film get_all genre')
    testsconfig = await read_json_data('movie_get_all_genre.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        docs = await genre.get_all_genre(**test['parameter'])
        assert len(docs) == int(test['lenght'])
        if test['body'] != '':
            assert docs == [SFilmGenre(**doc) for doc in await read_json_data('genre/' + test['body'])]
        logger.info(f"{test['name']} passed")
    logger.info('end test film get_all genre')


@pytest.mark.asyncio
async def test_films_bad_parameter_Genre_class(genre: genre_db.Genre):
    logger.info('start test bad parameter')
    assert await genre.get_genre_by_id('not_found') is None
    try:
        await genre.get_genre_by_id()
    except Exception as err:
        assert err.__class__ == TypeError, err
    try:
        await genre.get_all_genre()
    except Exception as err:
        assert err.__class__ == TypeError, err
    logger.info('end test bad parameter')
