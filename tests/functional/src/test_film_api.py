import pytest

from loguru import logger

# test get_all_film
#   elastic pagination bigger than 10000 is not allowed
#   https://www.elastic.co/guide/en/elasticsearch/guide/current/pagination.html
#   https://stackoverflow.com/questions/35206409/elasticsearch-2-1-result-window-is-too-large-index-max-result-window/35221900#35221900
#   https://stackoverflow.com/questions/41677198/result-window-is-too-large-from-size-must-be-less-than-or-equal-to-10000-b
#   curl -XPUT "http://localhost:9200/my_index/_settings" -d '{ "index" : { "max_result_window" : 500000 } }' -H "Content-Type: application/json"
#   test filter[genre]
#   test sort by imdb_rating
#   test page[size]
#       size = default
#       size = -1
#       size = 0
#       size = 1
#       size = 50
#       size = 1000
#   test page[number]
#       number = default
#       number = -1
#       number = 0
#       number = 1
#       number = 1000
# test search film
# test get film by id

@pytest.mark.asyncio
async def test_film(make_get_request):
    # Выполнение запроса
    response = await make_get_request('film')

    logger.debug('do response test')

    # Проверка результата
    assert response.status == 200
    logger.info('pass response test')
    assert len(response.body) == 50
    logger.info('response lenght is ok')
    #assert response.body == expected
