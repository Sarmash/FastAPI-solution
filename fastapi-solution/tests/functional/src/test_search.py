import pytest

from .data import es_data_films


@pytest.mark.parametrize(
    "query_data, expected_answer, es_data_films",
    [
        ({"query": "The Star"}, {"status": 200, "length": 50}, es_data_films),
        ({"query": "Mashed potato"}, {"status": 404, "length": 1}, es_data_films),
    ],
)
@pytest.mark.asyncio
async def test_search(
    make_get_request,
    es_data_films,
    es_write_data,
    query_data: dict,
    expected_answer: dict,
):

    await es_write_data(es_data_films)

    response = await make_get_request("films/search/", query_data)
    body = await response.json()

    assert response.status == expected_answer["status"]
    assert len(body) == expected_answer["length"]
