from operator import itemgetter

import pytest

from ..settings import test_settings
from ..testdata.data import MOVIES


@pytest.mark.parametrize(
    "expected_answer, data, url",
    [
        (
            {"status": 200},
            MOVIES,
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
        ),
        (
            {"status": 200},
            MOVIES,
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
        ),
    ],
)
@pytest.mark.asyncio
async def test_films_list_200(
    make_get_request_url,
    es_write_data,
    elastic_search_list_fixture,
    redis_get_fixture,
    es_delete_data,
    redis_delete_fixture,
    expected_answer: dict,
    data: dict,
    url: str,
):
    """Проверка работоспособности эндпоинтов localhost/api/v1/films
    на совпадение данных возвращаемых клиенту и данных из редиса и эластика"""
    await es_write_data(data, test_settings.movies_index)
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
    await es_delete_data(test_settings.movies_index)
    await redis_delete_fixture(url)

    assert response.status == expected_answer["status"]
    assert len(elastic_films) == len(response_films) == len(redis_films)
    assert result


@pytest.mark.parametrize(
    "expected_answer, data, url, url_id",
    [
        (
            {"status": 200},
            MOVIES,
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
            "c0142274-dc57-4a3a-a8fe-4c0a229c60f8",
        ),
        (
            {"status": 200},
            MOVIES,
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
            "c5dc6c27-1c24-4965-8acc-ae7dcd20801c",
        ),
        (
            {"status": 200},
            MOVIES,
            f"{test_settings.service_url}{test_settings.movies_endpoint}",
            "c0142274-dc57-4a3a-a8fe-4c0a229c60f1",
        ),
    ],
)
@pytest.mark.asyncio
async def test_films_list(
    make_get_request_url,
    es_write_data,
    elastic_search_list_fixture,
    redis_get_fixture,
    es_delete_data,
    redis_delete_fixture,
    expected_answer: dict,
    data: dict,
    url: str,
    url_id: str,
):
    """Проверка работоспособности эндпоинтов localhost/api/v1/films/{films_id}
    на совпадение данных возвращаемых клиенту и данных из редиса и эластика"""
    await es_write_data(data, test_settings.movies_index)
    url_address = f"{url}{url_id}"
    response = await make_get_request_url(url_address)
    response_films = await response.json()
    elastic = await elastic_search_list_fixture(test_settings.movies_index, id=url_id)
    elastic_films = {}
    for key, value in elastic.items():
        if key not in ("writers_names", "actors_names"):
            elastic_films[key] = value
    redis_films = await redis_get_fixture(url_address)
    await es_delete_data(test_settings.movies_index)
    await redis_delete_fixture(url_address)

    assert response.status == expected_answer["status"]
    assert len(elastic_films) == len(response_films) == len(redis_films)
    assert elastic_films == response_films == redis_films


@pytest.mark.parametrize(
    "url, code_result, data",
    [
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}?page[number]=0&page[size]=5",
            422,
            MOVIES,
        ),
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}?page[number]=-5&page[size]=5",
            422,
            MOVIES,
        ),
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}?page[number]=10&page[size]=10",
            404,
            MOVIES,
        ),
        (
            f"{test_settings.service_url}{test_settings.movies_endpoint}/c0142274-dc57-4a3a-a8fe-4c0a229c6005",
            404,
            MOVIES,
        ),
    ],
)
@pytest.mark.asyncio
async def test_genre_list_422(
    make_get_request_url,
    es_write_data,
    es_delete_data,
    redis_delete_fixture,
    url: str,
    code_result: int,
    data: dict,
):
    """Крайние случаи получения некорректного ввода пагинации.
    Запрос несуществующей страницы пагинации.
    Проверка запроса с некорректным идентификатором фильма."""
    await es_write_data(data, test_settings.movies_index)
    response_api = await make_get_request_url(url)
    await es_delete_data(test_settings.movies_index)
    await redis_delete_fixture(url)

    assert response_api.status == code_result
