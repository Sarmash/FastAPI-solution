from http import HTTPStatus

import pytest

from ..settings import test_settings
from ..testdata.http_exeptions import PERSON_NOT_FOUND
from ..utils.helpers import elastic_search_by_id, redis_get


@pytest.mark.asyncio
async def test_person(
    es_write_persons,
    redis_delete_fixture,
    redis_client,
    es_write_movies,
    session_client,
    es_client,
):
    """
    Тест запроса существующей персоны
    """
    url = f"{test_settings.service_url}{test_settings.persons_endpoint}111"
    response = await session_client.get(url)
    body = await response.json()
    response_elastic = await elastic_search_by_id(
        es_client, test_settings.persons_index, "111"
    )
    response_redis = await redis_get(redis_client, f"{url}/")
    assert response.status == HTTPStatus.OK
    assert len(body) == 1
    assert body[0]["id"] == response_elastic["id"] == response_redis[0]["id"]
    await redis_delete_fixture()


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [({"id": "999"}, {"status": HTTPStatus.NOT_FOUND, "message": PERSON_NOT_FOUND})],
)
@pytest.mark.asyncio
async def test_person_not_found(
    session_client,
    query_data,
    expected_answer,
):
    """
    Тест запроса несуществующей персоны
    """
    url = (
        f"{test_settings.service_url}{test_settings.persons_endpoint}"
        f"{query_data['id']}"
    )
    response = await session_client.get(url)
    body = await response.json()
    assert response.status == expected_answer["status"]
    assert body["detail"] == expected_answer["message"]


@pytest.mark.asyncio
async def test_pagination_200(
    session_client,
    redis_delete_fixture,
    es_write_persons,
    es_write_movies,
    redis_client,
):
    """
    Тест корректной работы пагинцации, запрос существующей страницы
    """

    url = (
        f"{test_settings.service_url}{test_settings.persons_endpoint}"
        f"search?query=Ben&page[number]=1&page[size]=1"
    )
    response = await session_client.get(url)
    response_redis = await redis_get(
        redis_client,
        f"{test_settings.service_url}"
        f"{test_settings.persons_endpoint}"
        f"search?query=Ben&page%5Bnumber%5D=1&page%5Bsize%5D=1",
    )
    body = await response.json()
    assert len(body) == len(response_redis) == 1

    await redis_delete_fixture()


@pytest.mark.asyncio
async def test_pagination_404(session_client):
    """
    Тест пагинцации, запрос несуществующей страницы
    """

    url = (
        f"{test_settings.service_url}{test_settings.persons_endpoint}"
        f"search?query=Ben&page[number]=2&page[size]=5"
    )
    response = await session_client.get(url)
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "params, status_code",
    [
        (
            f"{test_settings.service_url}{test_settings.persons_endpoint}"
            f"search?query=Ben&page[number]=0&page[size]=5",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            f"{test_settings.service_url}{test_settings.persons_endpoint}"
            f"search?query=Ben&page[number]=-1&page[size]=5",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
@pytest.mark.asyncio
async def test_pagination_422(
    session_client,
    params,
    status_code
):
    """
    Крайние случаи получения некорректного ввода пагинации
    """
    response = await session_client.get(params)
    assert response.status == status_code

    response_api = await session_client.get(params)
    assert response_api.status == status_code
