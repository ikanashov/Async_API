from loguru import logger

import pytest


@pytest.mark.asyncio
async def test_person(make_get_request, read_json_data):
    testsconfig = await read_json_data('person/config.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('person', params=test['parameter'])
        assert response.status == int(test['status']), test
        assert len(response.body) == int(test['lenght']), test
        if test['body'] != '':
            assert response.body == await read_json_data('person/' + test['body']), test
        logger.info(f"{test['name']} passed")

"""
@pytest.mark.asyncio
async def test_get_film_by_id(make_get_request, read_json_data):
    testsconfig = await read_json_data('film/config_get_by_id.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('film/' + test['film_id'])
        assert response.status == int(test['status']), test
        assert len(response.body) == int(test['lenght']), test
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body']), test
        logger.info(f"{test['name']} passed")


@pytest.mark.asyncio
async def test_film_search(make_get_request, read_json_data):
    testsconfig = await read_json_data('film/config_search.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('film', method='/search', params=test['parameter'])
        assert response.status == int(test['status']), test
        assert len(response.body) == int(test['lenght']), test
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body']), test
        logger.info(f"{test['name']} passed")
"""