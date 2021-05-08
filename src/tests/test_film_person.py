from loguru import logger

import pytest

from models.film import SFilmPersonDetail

from services import person as person_db


@pytest.fixture(scope='module')
async def person(conf, datastore):
    logger.info('setup person class')
    person_db.datastore = datastore
    person = person_db.Person()
    await person.set_person_index(conf.ELASTIC_PERSON_INDEX)
    yield person
    logger.info('end setup person class')


@pytest.mark.asyncio
async def test_film_Movie_Class(conf, person: person_db.Person, cache, redis, read_json_data):
    logger.info('test film person class')
    datas = await read_json_data('es_persons_data.json')
    for data in datas:
        await redis.delete(cache.genkey(index=conf.ELASTIC_PERSON_INDEX, id=data['id']))
        doc = await person.get_person_by_id(data['id'])
        cache_doc = await cache.get_data(index=conf.ELASTIC_PERSON_INDEX, id=data['id'])
        assert doc == SFilmPersonDetail(**data)
        assert doc == SFilmPersonDetail(**cache_doc)
    logger.info('end test film person class')

"""
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
"""

@pytest.mark.asyncio
async def test_films_bad_parameter_Person_class(person: person_db.Person):
    logger.info('start test bad parameter')
    assert await person.get_person_by_id('not_found') is None
    try:
        await person.get_person_by_id()
    except Exception as err:
        assert err.__class__ == TypeError, err
    try:
        await person.search_person()
    except Exception as err:
        assert err.__class__ == TypeError, err
    try:
        await person.get_all_person()
    except Exception as err:
        assert err.__class__ == TypeError, err
    logger.info('end test bad parameter')
