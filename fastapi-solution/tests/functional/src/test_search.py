import pytest

from ..settings import test_settings
from .data import es_data_films


@pytest.mark.parametrize(
    "query_data, expected_answer, data, url",
    [
        (
            {"query": "The Star"},
            {"status": 200, "length": 50},
            es_data_films,
            "search/",
        ),
        (
            {"query": "Mashed potato"},
            {"status": 404, "length": 1},
            es_data_films,
            "search/",
        ),
    ],
)
@pytest.mark.asyncio
async def test_search(
    make_get_request,
    data,
    es_write_data,
    es_delete_data,
    redis_delete_fixture,
    query_data: dict,
    expected_answer: dict,
    url: str,
):
    url_address = f"{test_settings.service_url}{test_settings.movies_endpoint}{url}"
    await es_write_data(data)
    response = await make_get_request(url_address, query_data)
    response_address = str(response.url)
    print(response_address)
    body = await response.json()
    await es_delete_data(test_settings.movies_index)
    await redis_delete_fixture(response_address)

    assert response.status == expected_answer["status"]
    assert len(body) == expected_answer["length"]
