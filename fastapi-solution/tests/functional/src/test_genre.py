import pytest

from ..settings import test_settings
from ..testdata.data import GENRES
from ..utils.helpers import elastic_search_by_id, elastic_search_list, redis_get


@pytest.mark.asyncio
async def test_genre_list_200(
    session_client, es_client, redis_client, es_write_data, es_delete_data
):
    """Проверка работоспособности ендпоинта localhost/api/v1/genres
    на совпадение данных возвращаемых клиенту и данных из редиса и еластика"""
    await es_write_data(GENRES, test_settings.genres_index)
    response_api = await session_client.get(
        f"{test_settings.service_url}{test_settings.genres_endpoint}"
    )
    assert response_api.status == 200
    response_api = await response_api.json()

    response_elastic = await elastic_search_list(
        client=es_client, index=test_settings.genres_index
    )

    response_redis = await redis_get(
        redis_client, f"{test_settings.service_url}{test_settings.genres_endpoint}"
    )
    await es_delete_data(test_settings.genres_index)
    assert len(response_api) == len(response_elastic) == len(response_redis)

    assert (
        {i["id"] for i in response_api}
        == {i["id"] for i in response_elastic}
        == {i["id"] for i in response_redis}
    )
    assert (
        {i["genre"] for i in response_api}
        == {i["genre"] for i in response_elastic}
        == {i["genre"] for i in response_redis}
    )


@pytest.mark.parametrize(
    "response, code_result",
    [
        (
            f"{test_settings.service_url}{test_settings.genres_endpoint}?page[number]=0&page[size]=5",
            422,
        ),
        (
            f"{test_settings.service_url}{test_settings.genres_endpoint}?page[number]=-1&page[size]=5",
            422,
        ),
    ],
)
@pytest.mark.asyncio
async def test_genre_list_422(session_client, response, code_result):
    """Крайние случаи получения некорректного ввода пагинации"""

    response_api = await session_client.get(response)
    assert response_api.status == code_result

    response_api = await session_client.get(response)
    assert response_api.status == code_result


@pytest.mark.asyncio
async def test_genre_list_404(session_client, es_write_data, es_delete_data):
    """Запрос несуществующей страницы пагинации"""

    await es_write_data(GENRES, test_settings.genres_index)
    response_api = await session_client.get(
        f"{test_settings.service_url}"
        f"{test_settings.genres_endpoint}"
        f"?page[number]=10&page[size]=10"
    )
    assert response_api.status == 404
    await es_delete_data(test_settings.genres_index)


@pytest.mark.parametrize(
    "genre_id, status_code",
    [(GENRES[0]["id"], 200), (GENRES[1]["id"], 200), (GENRES[2]["id"], 200)],
)
@pytest.mark.asyncio
async def test_genre_by_id_200(
    session_client,
    es_client,
    redis_client,
    genre_id,
    status_code,
    es_write_data,
    es_delete_data,
):
    """Проверка работоспособности ендпоинта localhost/api/v1/genres/{id_genre}
    на совпадение данных возвращаемых клиенту и данных из редиса и еластика"""
    await es_write_data(GENRES, test_settings.genres_index)

    response_api = await session_client.get(
        f"{test_settings.service_url}{test_settings.genres_endpoint}{genre_id}"
    )
    assert response_api.status == status_code
    response_api = await response_api.json()

    response_elastic = await elastic_search_by_id(
        es_client, test_settings.genres_index, genre_id
    )
    await es_delete_data(test_settings.genres_index)
    response_redis = await redis_get(
        redis_client,
        f"{test_settings.service_url}" f"{test_settings.genres_endpoint}" f"{genre_id}",
    )

    assert response_api["id"] == response_elastic["id"] == response_redis["id"]


@pytest.mark.asyncio
async def test_genre_by_id_404(session_client):
    """Проверка запроса с некорректным идентификатором жанра"""

    response_api = await session_client.get(
        f"{test_settings.service_url}{test_settings.genres_endpoint}/bad_genre_id"
    )
    assert response_api.status == 404
