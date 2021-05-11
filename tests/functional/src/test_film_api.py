from loguru import logger

import pytest


#   For future development
#   It's necessary to consider that
#   elastic pagination bigger than 10000 is not allowed by default
#   https://www.elastic.co/guide/en/elasticsearch/guide/current/pagination.html
#   https://stackoverflow.com/questions/35206409/elasticsearch-2-1-result-window-is-too-large-index-max-result-window/35221900#35221900
#   https://stackoverflow.com/questions/41677198/result-window-is-too-large-from-size-must-be-less-than-or-equal-to-10000-b
#   curl -XPUT "http://localhost:9200/my_index/_settings" -d
#   '{ "index" : { "max_result_window" : 500000 } }' -H "Content-Type: application/json"

@pytest.mark.asyncio
async def test_film(make_get_request, read_json_data):
    testsconfig = await read_json_data('film/config.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('film', params=test['parameter'])
        assert response.status == test['status'], test
        assert len(response.body) == test['lenght'], test
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body']), test
        logger.info(f"{test['name']} passed")


@pytest.mark.asyncio
async def test_get_film_by_id(make_get_request, read_json_data):
    testsconfig = await read_json_data('film/config_get_by_id.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('film/' + test['film_id'])
        assert response.status == test['status'], test
        assert len(response.body) == test['lenght'], test
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body']), test
        logger.info(f"{test['name']} passed")


@pytest.mark.asyncio
async def test_film_search(make_get_request, read_json_data):
    testsconfig = await read_json_data('film/config_search.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('film', method='/search', params=test['parameter'])
        assert response.status == test['status'], test
        assert len(response.body) == test['lenght'], test
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body']), test
        logger.info(f"{test['name']} passed")
