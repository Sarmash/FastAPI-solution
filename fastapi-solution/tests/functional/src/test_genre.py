import json

import pytest

from ..utils.helpers import elastic_search_list, elastic_search_by_id
from ..testdata.filling_elastic_genre import GENRES


@pytest.mark.asyncio
async def test_genre_list_200(http_client, elastic_client, redis_client):
    response_api = await http_client.get("http://fastapi:8000/api/v1/genres/")
    assert response_api.status == 200
    response_api = await response_api.json()

    response_elastic = await elastic_search_list(client=elastic_client,
                                                 index='genres',
                                                 size=50)

    response_redis = await redis_client.get("http://fastapi:8000/api/v1/genres/")
    assert isinstance(response_redis, bytes)
    response_redis = json.loads(response_redis)
    response_redis = [json.loads(item) for item in response_redis]

    assert len(response_api) == len(response_elastic) == len(response_redis)

    assert {i['id'] for i in response_api} == \
           {i['id'] for i in response_elastic} == \
           {i['id'] for i in response_redis}
    assert {i['genre'] for i in response_api} == \
           {i['genre'] for i in response_elastic} == \
           {i['genre'] for i in response_redis}


@pytest.mark.parametrize(
    "response, code_result", [
        ("http://fastapi:8000/api/v1/genres/?page[number]=0&page[size]=5", 422),
        ("http://fastapi:8000/api/v1/genres/?page[number]=-1&page[size]=5", 422)
    ]
)
@pytest.mark.asyncio
async def test_genre_list_422(http_client, response, code_result):
    response_api = await http_client.get(response)
    assert response_api.status == code_result

    response_api = await http_client.get(response)
    assert response_api.status == code_result


@pytest.mark.asyncio
async def test_genre_list_404(http_client):
    response_api = await http_client.get("http://fastapi:8000/api/v1/genres/?page[number]=10&page[size]=10")
    assert response_api.status == 404


@pytest.mark.parametrize(
    "genre_id, status_code", [
        (GENRES[0]['id'], 200),
        (GENRES[1]['id'], 200),
        (GENRES[2]['id'], 200)
    ]
)
@pytest.mark.asyncio
async def test_genre_by_id_200(http_client, elastic_client, redis_client, genre_id, status_code):
    response_api = await http_client.get(f"http://fastapi:8000/api/v1/genres/{genre_id}")
    assert response_api.status == status_code
    response_api = await response_api.json()

    response_elastic = await elastic_search_by_id(elastic_client, 'genres', genre_id)

    response_redis = await redis_client.get(f"http://fastapi:8000/api/v1/genres/{genre_id}")
    assert isinstance(response_redis, bytes)
    response_redis = json.loads(response_redis)

    assert response_api['id'] == response_elastic['id'] == response_redis['id']
