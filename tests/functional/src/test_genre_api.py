from loguru import logger

import pytest


@pytest.mark.asyncio
async def test_genre(make_get_request, read_json_data):
    testsconfig = await read_json_data('genre/config.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('genre', params=test['parameter'])
        assert response.status == int(test['status']), test
        assert len(response.body) == int(test['lenght']), test
        if test['body'] != '':
            assert response.body == await read_json_data('genre/' + test['body']), test
        logger.info(f"{test['name']} passed")

"""
@pytest.mark.asyncio
async def test_get_person_by_id(make_get_request, read_json_data):
    testsconfig = await read_json_data('person/config_get_by_id.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('person/' + test['person_id'])
        assert response.status == int(test['status']), test
        assert len(response.body) == int(test['lenght']), test
        if test['body'] != '':
            assert response.body == await read_json_data('person/' + test['body']), test
        logger.info(f"{test['name']} passed")
"""