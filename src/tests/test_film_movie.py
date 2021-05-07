from loguru import logger

import pytest

from models.film import SFilm

from services import movie as mov_db


@pytest.fixture(scope='module')
async def movie(conf, datastore):
    logger.info('setup movie class')
    mov_db.datastore = datastore
    movie = mov_db.Movie()
    await movie.set_movie_index(conf.ELASTIC_INDEX)
    yield movie
    logger.info('end setup movie class')


@pytest.mark.asyncio
async def test_film_Movie_Class(conf, movie: mov_db.Movie, cache, redis, read_json_data):
    logger.info('test film movie class')
    datas = await read_json_data('es_films_data.json')
    for data in datas:
        await redis.delete(cache.genkey(index=conf.ELASTIC_INDEX, id=data['id']))
        doc = await movie.get_film_by_id(data['id'])
        cache_doc = await cache.get_data(index=conf.ELASTIC_INDEX, id=data['id'])
        assert doc == SFilm(**data)
        assert doc == SFilm(**cache_doc)
    logger.info('end test film movie class')


@pytest.mark.asyncio
async def test_films_search_Movie_Class(movie: mov_db.Movie, read_json_data):
    logger.info('test films search movie')
    testsconfig = await read_json_data('movie_search.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        docs = await movie.search_film(**test['parameter'])
        assert len(docs) == int(test['lenght'])
        if test['body'] != '':
            assert docs == [SFilm(**doc) for doc in await read_json_data('movie/' + test['body'])]
        logger.info(f"{test['name']} passed")
    logger.info('end test films search movie')


@pytest.mark.asyncio
async def test_films_get_all_film_Movie_Class(movie: mov_db.Movie, read_json_data):
    logger.info('test films get_all movie')
    testsconfig = await read_json_data('movie_get_all_film.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        docs = await movie.get_all_film(**test['parameter'])
        assert len(docs) == int(test['lenght'])
        if test['body'] != '':
            assert docs == [SFilm(**doc) for doc in await read_json_data('movie/' + test['body'])]
        logger.info(f"{test['name']} passed")
    logger.info('end test films get_all movie')


@pytest.mark.asyncio
async def test_films_bad_parameter_Movie_class(movie: mov_db.Movie):
    logger.info('start test bad parameter')
    assert await movie.get_film_by_id('not_found') is None
    try:
        await movie.get_film_by_id()
    except Exception as err:
        assert err.__class__ == TypeError, err
    try:
        await movie.search_film()
    except Exception as err:
        assert err.__class__ == TypeError, err
    try:
        await movie.get_all_film()
    except Exception as err:
        assert err.__class__ == TypeError, err
    logger.info('end test bad parameter')
