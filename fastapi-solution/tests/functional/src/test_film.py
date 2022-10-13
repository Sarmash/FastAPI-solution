from operator import itemgetter

import pytest

from ..settings import test_settings


@pytest.mark.parametrize(
    "expected_answer, url",
    [
        (
            {"status": 200},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
        ),
        (
            {"status": 200},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
        ),
    ],
)
@pytest.mark.asyncio
async def test_films_list_200(
    es_write_movies,
    make_get_request_url,
    elastic_search_list_fixture,
    redis_get_fixture,
    redis_delete_fixture,
    expected_answer: dict,
    url: str,
):
    """Проверка работоспособности эндпоинтов localhost/api/v1/films
    на совпадение данных возвращаемых клиенту и данных из редиса и эластика"""
    response = await make_get_request_url(url)
    response_films = await response.json()
    elastic = await elastic_search_list_fixture(test_settings.movies_index)
    elastic_films = [
        {"id": i["id"], "title": i["title"], "imdb_rating": i["imdb_rating"]}
        for i in elastic
    ]
    redis_films = await redis_get_fixture(url)
    response_films, redis_films, elastic_films = [
        sorted(_, key=itemgetter("id"))
        for _ in (response_films, redis_films, elastic_films)
    ]
    pairs = zip(response_films, redis_films, elastic_films)
    result = True if all(x == y and x == z for x, y, z in pairs) else False
    await redis_delete_fixture(url)

    assert response.status == expected_answer["status"]
    assert len(elastic_films) == len(response_films) == len(redis_films)
    assert result


@pytest.mark.parametrize(
    "expected_answer, url, url_id",
    [
        (
            {"status": 200},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
            "c0142274-dc57-4a3a-a8fe-4c0a229c60f8",
        ),
        (
            {"status": 200},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
            "c5dc6c27-1c24-4965-8acc-ae7dcd20801c",
        ),
        (
            {"status": 200},
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
            "c0142274-dc57-4a3a-a8fe-4c0a229c60f1",
        ),
    ],
)
@pytest.mark.asyncio
async def test_films_list(
    es_write_movies,
    make_get_request_url,
    elastic_search_list_fixture,
    redis_get_fixture,
    redis_delete_fixture,
    expected_answer: dict,
    url: str,
    url_id: str,
):
    """Проверка работоспособности эндпоинтов localhost/api/v1/films/{films_id}
    на совпадение данных возвращаемых клиенту и данных из редиса и эластика"""
    url_address = f"{url}{url_id}"
    response = await make_get_request_url(url_address)
    response_films = await response.json()
    elastic = await elastic_search_list_fixture(test_settings.movies_index, id=url_id)
    elastic_films = {}
    for key, value in elastic.items():
        if key not in ("writers_names", "actors_names"):
            elastic_films[key] = value
    redis_films = await redis_get_fixture(url_address)
    await redis_delete_fixture(url_address)

    assert response.status == expected_answer["status"]
    assert len(elastic_films) == len(response_films) == len(redis_films)
    assert elastic_films == response_films == redis_films


@pytest.mark.parametrize(
    "url, code_result",
    [
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}?page[number]=0&page[size]=5",
            422,
        ),
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}?page[number]=-5&page[size]=5",
            422,
        ),
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}?page[number]=10&page[size]=10",
            404,
        ),
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}/c0142274-dc57-4a3a-a8fe-4c0a229c6005",
            404,
        ),
    ],
)
@pytest.mark.asyncio
async def test_genre_list_422(
    es_write_movies,
    make_get_request_url,
    redis_delete_fixture,
    url: str,
    code_result: int,
):
    """Крайние случаи получения некорректного ввода пагинации.
    Запрос несуществующей страницы пагинации.
    Проверка запроса с некорректным идентификатором фильма."""
    response_api = await make_get_request_url(url)
    await redis_delete_fixture(url)

    assert response_api.status == code_result
