from http import HTTPStatus

import pytest

from ..settings import test_settings
from ..testdata.http_exeptions import FILM_NOT_FOUND
from ..utils.helpers import redis_get, elastic_search_list, http_request


@pytest.mark.parametrize(
    "query, status_code",
    [
        ("Suzy", HTTPStatus.OK),
        ("Angela", HTTPStatus.OK),
        ("who", HTTPStatus.OK),
        ("star", HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
async def test_films_search_200(
    session_client,
    es_client,
    redis_client,
    query,
    status_code,
    redis_delete_fixture,
    es_write_persons,
    es_write_movies,
):
    """
    Проверка поиска фильмов по актеру, сценаристу, части описания и части названия.
    Проверка совпадения ответа от сервиса и данных в еластике, так же проверка записи
    полученных данных в Редис

    Актер = 'Suzy Stokey'
    Сценарист = 'Angela Turner'
    Часть описания = 'who'
    Часть заголовка = star
    """
    request_url = (
        f"{test_settings.service_url}"
        f"{test_settings.search_films_endpoint}"
        f"?query={query}"
    )

    response_api = await http_request(session_client, request_url, status_code)

    response_elastic = await elastic_search_list(
        es_client,
        index=test_settings.movies_index,
        body={
            "_source": {"includes": ["id", "title", "imdb_rating"]},
            "query": {
                "query_string": {"query": query},
            },
        },
    )
    response_redis = await redis_get(redis_client, request_url)

    assert (
        {i["id"] for i in response_api}
        == {i["id"] for i in response_elastic}
        == {i["id"] for i in response_redis}
    )
    await redis_delete_fixture()


@pytest.mark.parametrize(
    "query, status_code, movies, size",
    [
        ("star", HTTPStatus.OK, 3, 3),
        ("star", HTTPStatus.OK, 4, 4),
        ("star", HTTPStatus.OK, 5, 5),
    ],
)
@pytest.mark.asyncio
async def test_pagination_films_search_200(
    session_client,
    query,
    size,
    status_code,
    movies,
    redis_delete_fixture,
    es_write_persons,
    es_write_movies,
):
    """Проверка вывода N-го числа данных с помощью пагинации"""

    request_url = (
        f"{test_settings.service_url}"
        f"{test_settings.search_films_endpoint}"
        f"?query={query}&page[number]=1&page[size]={size}"
    )

    response_api = await http_request(session_client, request_url, status_code)

    assert len(response_api) == movies == size
    await redis_delete_fixture()


@pytest.mark.parametrize(
    "query, status_code",
    [
        ("?query=123", HTTPStatus.NOT_FOUND),
        ("?query=%*&", HTTPStatus.NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_films_search_404(session_client, query, status_code):
    """Проверка крайних случаев ошибки в запросе"""

    request_url = (
        f"{test_settings.service_url}"
        f"{test_settings.search_films_endpoint}"
        f"{query}"
    )

    response_api = await http_request(session_client, request_url, status_code)

    assert response_api["detail"] == FILM_NOT_FOUND


@pytest.mark.parametrize(
    "query, status_code",
    [
        ("Suzy+Stokey", HTTPStatus.OK),
        ("Fred+Olen+Ray", HTTPStatus.OK),
        ("Sandy+Brooke", HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
async def test_person_search_200(
    session_client,
    es_client,
    redis_client,
    query,
    status_code,
    es_write_persons,
    es_write_movies,
    redis_delete_fixture,
):
    """Проверка совпадения данных выводимых при запросе данных для искомой персоны"""
    request_url = (
        f"{test_settings.service_url}"
        f"{test_settings.search_persons_endpoint}"
        f"?query={query}"
    )

    response_api = await http_request(session_client, request_url, status_code)

    response_elastic = await elastic_search_list(
        es_client,
        index=test_settings.persons_index,
        body={"query": {"match": {"full_name": query}}},
    )

    response_redis = await redis_get(redis_client, request_url)

    assert (
        {i["id"] for i in response_api}
        == {i["id"] for i in response_elastic}
        == {i["id"] for i in response_redis}
    )

    body = {
        "query": {
            "multi_match": {
                "query": query,
                "type": "best_fields",
                "fields": ["actors_names", "writers_names", "director"],
            }
        }
    }

    response_elastic = await elastic_search_list(
        es_client, index=test_settings.movies_index, body=body
    )
    response_film_ids = set()
    for film in response_api:
        for j in film["film_ids"]:
            response_film_ids.add(j)

    assert response_film_ids == {film["id"] for film in response_elastic}
    await redis_delete_fixture()


@pytest.mark.parametrize(
    "query, status_code, films, size",
    [("Fred+Olen+Ray", HTTPStatus.OK, 1, 1), ("Suzy+Stokey", HTTPStatus.OK, 2, 2)],
)
@pytest.mark.asyncio
async def test_pagination_persons_search_200(
    session_client,
    query,
    size,
    status_code,
    films,
    redis_delete_fixture,
    es_write_persons,
    es_write_movies,
):
    """Проверка вывода N-го числа данных с помощью пагинации"""

    request_url = (
        f"{test_settings.service_url}"
        f"{test_settings.search_films_endpoint}"
        f"?query={query}&page[number]=1&page[size]={size}"
    )

    response_api = await http_request(session_client, request_url, status_code)
    assert len(response_api) == films == size
    await redis_delete_fixture()


@pytest.mark.parametrize(
    "query, status_code",
    [
        ("?query=124563", HTTPStatus.NOT_FOUND),
        ("?query=%fdskgj", HTTPStatus.NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_person_search_404(session_client, query, status_code):
    """Проверка крайних случаев ошибки в запросе"""

    request_url = (
        f"{test_settings.service_url}"
        f"{test_settings.search_films_endpoint}"
        f"{query}"
    )

    response_api = await http_request(session_client, request_url, status_code)
    assert response_api["detail"] == FILM_NOT_FOUND
