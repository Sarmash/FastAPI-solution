import pytest

from ..settings import test_settings
from ..utils.helpers import elastic_search_by_id
from .data import es_data_films, es_data_persons


@pytest.mark.asyncio
async def test_person(
        es_write_persons,
        es_write_data,
        session_client,
        es_client
):
    """
    Тест запроса существующей персоны
    """
    await es_write_data(es_data_films)
    await es_write_persons(es_data_persons)
    url = f"{test_settings.service_url}{test_settings.persons_endpoint}111"
    response = await session_client.get(url)
    body = await response.json()
    response_elastic = await elastic_search_by_id(
        es_client, test_settings.persons_index, "111"
    )
    assert response.status == 200
    assert len(body) == 1
    assert body[0]["id"] == response_elastic["id"]
    await es_client.delete_by_query(
        conflicts="proceed",
        index=test_settings.persons_index,
        body={"query": {"match_all": {}}},
    )


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [({"id": "999"}, {"status": 404, "message": "person not found"})],
)
@pytest.mark.asyncio
async def test_person_not_found(
    session_client,
    es_write_data,
    es_write_persons,
    es_client,
    query_data,
    expected_answer,
):
    """
    Тест запроса несуществующей персоны
    """
    await es_write_data(es_data_films)
    await es_write_persons(es_data_persons)
    url = (
        f"{test_settings.service_url}{test_settings.persons_endpoint}"
        f"{query_data['id']}"
    )
    response = await session_client.get(url)
    body = await response.json()
    assert response.status == expected_answer["status"]
    assert body["detail"] == expected_answer["message"]
    await es_client.delete_by_query(
        conflicts="proceed",
        index=test_settings.persons_index,
        body={"query": {"match_all": {}}},
    )


@pytest.mark.asyncio
async def test_pagination_200(
    session_client,
    es_write_data,
    es_write_persons,
    es_client,
):
    """
    Тест корректной работы пагинцации, запрос существующей страницы
    """
    await es_write_data(es_data_films)
    await es_write_persons(es_data_persons)

    url = (
        f"{test_settings.service_url}{test_settings.persons_endpoint}"
        f"search?query=Ben&page[number]=1&page[size]=1"
    )
    response = await session_client.get(url)
    body = await response.json()
    assert len(body) == 1

    await es_client.delete_by_query(
        conflicts="proceed",
        index=test_settings.persons_index,
        body={"query": {"match_all": {}}},
    )


@pytest.mark.asyncio
async def test_pagination_404(
    session_client,
    es_write_data,
    es_write_persons,
    es_client,
):
    """
    Тест пагинцации, запрос несуществующей страницы
    """
    await es_write_data(es_data_films)
    await es_write_persons(es_data_persons)

    url = (
        f"{test_settings.service_url}{test_settings.persons_endpoint}"
        f"search?query=Ben&page[number]=2&page[size]=5"
    )
    response = await session_client.get(url)
    assert response.status == 404

    await es_client.delete_by_query(
        conflicts="proceed",
        index=test_settings.persons_index,
        body={"query": {"match_all": {}}},
    )


@pytest.mark.parametrize(
    "params, status_code",
    [
        (
            f"{test_settings.service_url}{test_settings.persons_endpoint}"
            f"search?query=Ben&page[number]=0&page[size]=5",
            422,
        ),
        (
            f"{test_settings.service_url}{test_settings.persons_endpoint}"
            f"search?query=Ben&page[number]=-1&page[size]=5",
            422,
        ),
    ],
)
@pytest.mark.asyncio
async def test_pagination_422(
    session_client,
    params,
    status_code,
    es_write_data,
    es_write_persons,
    es_client,
):
    """
    Крайние случаи получения некорректного ввода пагинации
    """
    await es_write_data(es_data_films)
    await es_write_persons(es_data_persons)

    response = await session_client.get(params)
    assert response.status == status_code

    response_api = await session_client.get(params)
    assert response_api.status == status_code

    await es_client.delete_by_query(
        conflicts="proceed",
        index=test_settings.persons_index,
        body={"query": {"match_all": {}}},
    )