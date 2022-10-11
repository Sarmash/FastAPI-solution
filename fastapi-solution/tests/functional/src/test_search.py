import pytest
from ..testdata.http_exeptions import FILM_NOT_FOUND
from ..settings import test_settings
from ..utils.helpers import redis_get, elastic_search_list, http_request


@pytest.mark.parametrize(
    "query, status_code", [("Suzy", 200), ("Angela", 200), ("who", 200), ("star", 200)]
)
@pytest.mark.asyncio
async def test_films_search_200(
    session_client, es_client, redis_client, query, status_code
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


@pytest.mark.parametrize(
    "query, status_code, movies, size",
    [("star", 200, 3, 3), ("star", 200, 4, 4), ("star", 200, 5, 5)],
)
@pytest.mark.asyncio
async def test_pagination_films_search_200(
    session_client, query, size, status_code, movies
):
    """Проверка вывода N-го числа данных с помощью пагинации"""

    request_url = (
        f"{test_settings.service_url}"
        f"{test_settings.search_films_endpoint}"
        f"?query={query}&page[number]=1&page[size]={size}"
    )

    response_api = await http_request(session_client, request_url, status_code)

    assert len(response_api) == movies == size


@pytest.mark.parametrize(
    "query, status_code",
    [
        ("?query=123", 404),
        ("?query=%*&", 404),
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
    [("Suzy+Stokey", 200), ("Fred+Olen+Ray", 200), ("Sandy+Brooke", 200)],
)
@pytest.mark.asyncio
async def test_person_search_200(
    session_client, es_client, redis_client, query, status_code
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


@pytest.mark.parametrize(
    "query, status_code, films, size",
    [("Fred+Olen+Ray", 200, 1, 1), ("Suzy+Stokey", 200, 2, 2)],
)
@pytest.mark.asyncio
async def test_pagination_persons_search_200(
    session_client, query, size, status_code, films
):
    """Проверка вывода N-го числа данных с помощью пагинации"""

    request_url = (
        f"{test_settings.service_url}"
        f"{test_settings.search_films_endpoint}"
        f"?query={query}&page[number]=1&page[size]={size}"
    )

    response_api = await http_request(session_client, request_url, status_code)
    assert len(response_api) == films == size


@pytest.mark.parametrize(
    "query, status_code",
    [
        ("?query=124563", 404),
        ("?query=%fdskgj", 404),
    ],
)
@pytest.mark.asyncio
async def test_person_search_404(session_client, query, status_code, es_delete_data):
    """Проверка крайних случаев ошибки в запросе"""

    request_url = (
        f"{test_settings.service_url}"
        f"{test_settings.search_films_endpoint}"
        f"{query}"
    )

    response_api = await http_request(session_client, request_url, status_code)

    assert response_api["detail"] == FILM_NOT_FOUND
    await es_delete_data(index=test_settings.movies_index)
