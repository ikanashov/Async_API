import pytest

from loguru import logger

# test get_all_film
#   elastic pagination bigger than 10000 is not allowed
#   https://www.elastic.co/guide/en/elasticsearch/guide/current/pagination.html
#   https://stackoverflow.com/questions/35206409/elasticsearch-2-1-result-window-is-too-large-index-max-result-window/35221900#35221900
#   https://stackoverflow.com/questions/41677198/result-window-is-too-large-from-size-must-be-less-than-or-equal-to-10000-b
#   curl -XPUT "http://localhost:9200/my_index/_settings" -d '{ "index" : { "max_result_window" : 500000 } }' -H "Content-Type: application/json"
#   + test filter[genre]
#   + test sort by imdb_rating
#   test page[size]
#      + size = default
#       size = -1
#       size = 0
#       size = 1
#       + size = 50
#       size = 1000
#   test page[number]
#       + number = default
#       + number = -1
#       number = 0
#       + number = 1
#       number = 1000
# + test search film
# test get film by id

@pytest.mark.asyncio
async def test_film(make_get_request, read_json_data):
    # Имя файла надо убрать в конфиг
    testsconfig = await read_json_data('film/config.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('film', params = test['parameter'])
        assert response.status == int(test['status']), test
        #logger.info('pass response test'), test
        assert len(response.body) == int(test['lenght']), test
        #logger.info('response lenght is ok')
        #logger.debug(f'response body : {response.body}')
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body']), test
        logger.info(f"{test['name']} passed")

@pytest.mark.asyncio
async def test_get_film_by_id(make_get_request, read_json_data):
    # Имя файла надо убрать в конфиг
    testsconfig = await read_json_data('film/config_get_by_id.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('film/' + test['film_id'])
        assert response.status == int(test['status']), test
        #logger.info('pass response test'), test
        assert len(response.body) == int(test['lenght']), test
        #logger.info('response lenght is ok')
        #logger.debug(f'response body : {response.body}')
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body']), test
        logger.info(f"{test['name']} passed")

@pytest.mark.asyncio
async def test_film_search(make_get_request, read_json_data):
    # Имя файла надо убрать в конфиг
    testsconfig = await read_json_data('film/config_search.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        response = await make_get_request('film', method = '/search', params = test['parameter'])
        assert response.status == int(test['status']), test
        #logger.info('pass response test'), test
        assert len(response.body) == int(test['lenght']), test
        #logger.info('response lenght is ok')
        #logger.debug(f'response body : {response.body}')
        if test['body'] != '':
            assert response.body == await read_json_data('film/' + test['body']), test
        logger.info(f"{test['name']} passed")
