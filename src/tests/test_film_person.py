from loguru import logger

import pytest

from models.film import SFilmPersonDetail

from services.person import Person


@pytest.fixture(scope='module')
async def person(conf, datastore):
    logger.info('setup person class')
    person = Person(datastore)
    person.set_person_index(conf.ELASTIC_PERSON_INDEX)
    yield person
    logger.info('end setup person class')


@pytest.mark.asyncio
async def test_film_Person_Class(conf, person: Person, cache, redis, read_json_data):
    logger.info('test film person class')
    datas = await read_json_data('es_persons_data.json')
    for data in datas:
        await redis.delete(cache.genkey(index=conf.ELASTIC_PERSON_INDEX, id=data['id']))
        doc = await person.get_person_by_id(data['id'])
        cache_doc = await cache.get_data(index=conf.ELASTIC_PERSON_INDEX, id=data['id'])
        assert doc == SFilmPersonDetail(**data)
        assert doc == SFilmPersonDetail(**cache_doc)
    logger.info('end test film person class')


@pytest.mark.asyncio
async def test_films_search_Person_Class(person: Person, read_json_data):
    logger.info('test films search person')
    testsconfig = await read_json_data('person_search.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        docs = await person.search_person(**test['parameter'])
        assert len(docs) == int(test['lenght'])
        if test['body'] != '':
            assert docs == [SFilmPersonDetail(**doc) for doc in await read_json_data('person/' + test['body'])]
        logger.info(f"{test['name']} passed")
    logger.info('end test films search person')


@pytest.mark.asyncio
async def test_films_get_all_person_Person_Class(person: Person, read_json_data):
    logger.info('test films get_all person')
    testsconfig = await read_json_data('person_get_all.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        docs = await person.get_all_person(**test['parameter'])
        assert len(docs) == int(test['lenght'])
        if test['body'] != '':
            assert docs == [SFilmPersonDetail(**doc) for doc in await read_json_data('person/' + test['body'])]
        logger.info(f"{test['name']} passed")
    logger.info('end test films get_all person')


@pytest.mark.asyncio
async def test_films_bad_parameter_Person_class(person: Person):
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
