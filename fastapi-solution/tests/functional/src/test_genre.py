import json

import pytest

from ..utils.helpers import elastic_search_list


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


@pytest.mark.asyncio
async def test_genre_list_422(http_client):
    response_api = await http_client.get("http://fastapi:8000/api/v1/genres/?page[number]=0&page[size]=5")
    assert response_api.status == 422

    response_api = await http_client.get("http://fastapi:8000/api/v1/genres/?page[number]=-1&page[size]=5")
    assert response_api.status == 422


async def test_genre_list_404(http_client):
    response_api = await http_client.get("http://fastapi:8000/api/v1/genres/?page[number]=10&page[size]=10")
    assert response_api.status == 404


@pytest.mark.asyncio
async def test_genre_by_id():
    pass
