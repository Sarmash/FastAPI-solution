import aiohttp
import pytest

from ..settings import test_settings
from ..utils.helpers import elastic_search_list, elastic_search_by_id, redis_get

service_url: str = 'http://localhost:8000/api/v1/persons/search'


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': '111'},
                {'status': 200, 'length': 1}
        )]
)
@pytest.mark.asyncio
async def test_person(es_write_persons, session_client, es_client,
                      redis_client, query_data, expected_answer):
    """
    Тест запроса существующей персоны
    """
    es_data_persons = [{"id": '111', "full_name": "Ann"},
                       {"id": "222", "full_name": "Bob"},
                       {"id": '333', "full_name": 'Ben'},
                       {"id": '444', "full_name": 'Howard'}]
    es_write_persons(es_data_persons)
    url = f"{test_settings.service_url}{test_settings.persons_endpoint}"\
          f"{query_data['id']}"
    response = await session_client.get(url)
    body = await response.json()
    response_elastic = await elastic_search_by_id(
        es_client,
        test_settings.persons_index, id_=query_data['id'])
    response_redis = await redis_get(
        redis_client, f"{test_settings.service_url}"
                      f"{test_settings.persons_endpoint}"
    )
    assert response.status == expected_answer["status"]
    assert len(body) == expected_answer["length"]

    assert len(response) == len(response_elastic) == len(response_redis)
    assert {i['id'] for i in response} == \
           {i['id'] for i in response_elastic} == \
           {i['id'] for i in response_redis}
    assert {i['full_name'] for i in response} == \
           {i['full_name'] for i in response_elastic} == \
           {i['full_name'] for i in response_redis}


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': '999'},
                {'status': 404, 'message': 'person not found'}
        )]
)
@pytest.mark.asyncio
async def test_person(session_client, query_data, expected_answer):
    """
    Тест запроса несуществующей персоны
    """
    url = f"{test_settings.service_url}{test_settings.persons_endpoint}{query_data['id']}"
    response = await session_client.get(url)
    body = await response.json()
    assert response.status == expected_answer["status"]
    assert body['detail'] == expected_answer["message"]


@pytest.mark.asyncio
async def test_pagination_200(session_client):
    """
    Тест корректной работы пагинцации, запрос существующей страницы
    """
    url = f"{test_settings.service_url}{test_settings.persons_endpoint}"\
          f"search?query=Ben&page[number]=1&page[size]=1"
    response = await session_client.get(url)
    body = await response.json()
    assert len(body) == 1


@pytest.mark.asyncio
async def test_pagination_404(session_client):
    """
    Тест пагинцации, запрос несуществующей страницы
    """
    url = f"{test_settings.service_url}{test_settings.persons_endpoint}"\
          f"search?query=Ben&page[number]=2&page[size]=5"
    response = await session_client.get(url)
    assert response.status == 404


@pytest.mark.parametrize(
    "params, status_code", [
        (f"{test_settings.service_url}{test_settings.persons_endpoint}"
         f"search?query=Ben&page[number]=0&page[size]=5", 422),
        (f"{test_settings.service_url}{test_settings.persons_endpoint}"
         f"search?query=Ben&page[number]=-1&page[size]=5", 422)
    ]
)
@pytest.mark.asyncio
async def test_pagination_422(session_client, params, status_code):
    """
    Крайние случаи получения некорректного ввода пагинации
    """
    response = await session_client.get(params)
    assert response.status == status_code

    response_api = await session_client.get(params)
    assert response_api.status == status_code
