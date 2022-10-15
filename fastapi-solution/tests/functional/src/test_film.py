from http import HTTPStatus
from operator import itemgetter

import pytest

from ..settings import test_settings
from ..utils.helpers import (
    elastic_search_by_id,
    elastic_search_list,
    http_request,
    redis_get,
)


@pytest.mark.parametrize(
    "expected_answer, url",
    [
        (
            {"status": HTTPStatus.OK},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
        ),
        (
            {"status": HTTPStatus.OK},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
        ),
    ],
)
@pytest.mark.asyncio
async def test_films_list_200(
    es_write_movies,
    session_client,
    es_client,
    redis_client,
    redis_delete_fixture,
    expected_answer: dict,
    url: str,
):
    """Проверка работоспособности эндпоинтов localhost/api/v1/films
    на совпадение данных возвращаемых клиенту и данных из редиса и эластика"""
    response_films = await http_request(session_client, url, expected_answer["status"])
    elastic = await elastic_search_list(es_client, test_settings.movies_index)
    elastic_films = [
        {"id": i["id"], "title": i["title"], "imdb_rating": i["imdb_rating"]}
        for i in elastic
    ]
    redis_films = await redis_get(redis_client, url)
    response_films, redis_films, elastic_films = [
        sorted(_, key=itemgetter("id"))
        for _ in (response_films, redis_films, elastic_films)
    ]
    pairs = zip(response_films, redis_films, elastic_films)
    result = True if all(x == y and x == z for x, y, z in pairs) else False
    await redis_delete_fixture()

    assert len(elastic_films) == len(response_films) == len(redis_films)
    assert result


@pytest.mark.parametrize(
    "expected_answer, url, url_id",
    [
        (
            {"status": HTTPStatus.OK},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
            "c0142274-dc57-4a3a-a8fe-4c0a229c60f8",
        ),
        (
            {"status": HTTPStatus.OK},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
            "c5dc6c27-1c24-4965-8acc-ae7dcd20801c",
        ),
        (
            {"status": HTTPStatus.OK},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
            "c0142274-dc57-4a3a-a8fe-4c0a229c60f1",
        ),
    ],
)
@pytest.mark.asyncio
async def test_films_list(
    es_write_movies,
    session_client,
    es_client,
    redis_client,
    redis_delete_fixture,
    expected_answer: dict,
    url: str,
    url_id: str,
):
    """Проверка работоспособности эндпоинтов localhost/api/v1/films/{films_id}
    на совпадение данных возвращаемых клиенту и данных из редиса и эластика"""
    url_address = f"{url}{url_id}"
    response_films = await http_request(
        session_client, url_address, expected_answer["status"]
    )
    elastic = await elastic_search_by_id(
        es_client, test_settings.movies_index, id_=url_id
    )
    elastic_films = {}
    for key, value in elastic.items():
        if key not in ("writers_names", "actors_names"):
            elastic_films[key] = value
    redis_films = await redis_get(redis_client, url_address)
    await redis_delete_fixture()

    assert len(elastic_films) == len(response_films) == len(redis_films)
    assert elastic_films == response_films == redis_films


@pytest.mark.parametrize(
    "url, code_result",
    [
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}?page[number]=0&page[size]=5",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}?page[number]=-5&page[size]=5",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}?page[number]=10&page[size]=10",
            HTTPStatus.NOT_FOUND,
        ),
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}/c0142274-dc57-4a3a-a8fe-4c0a229c6005",
            HTTPStatus.NOT_FOUND,
        ),
    ],
)
@pytest.mark.asyncio
async def test_genre_list_422(
    es_write_movies,
    session_client,
    redis_delete_fixture,
    url: str,
    code_result: int,
):
    """Крайние случаи получения некорректного ввода пагинации.
    Запрос несуществующей страницы пагинации.
    Проверка запроса с некорректным идентификатором фильма."""
    response_api = await session_client.get(url)
    await redis_delete_fixture()

    assert response_api.status == code_result
