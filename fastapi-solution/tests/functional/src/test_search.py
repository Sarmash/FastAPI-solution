import uuid

import pytest


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "The Star"}, {"status": 200, "length": 50}),
        ({"query": "Mashed potato"}, {"status": 404, "length": 1}),
    ],
)
@pytest.mark.asyncio
async def test_search(make_get_request, es_write_data, query_data, expected_answer):
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "imdb_rating": 8.5,
            "genre": ["Action", "Sci-Fi"],
            "title": "The Star",
            "description": "New World",
            "director": "Stan",
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [
                {"id": "111", "name": "Ann"},
                {"id": "222", "name": "Bob"},
            ],
            "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
        }
        for _ in range(60)
    ]
    await es_write_data(es_data)

    response = await make_get_request("films/search/", query_data)

    # session = aiohttp.ClientSession()
    # url = test_settings.service_url + "films/search/"
    # query = query_data
    # async with session.get(url, params=query) as response:
    #     body = await response.json()
    #     # headers = response.json()
    #     status = response.status
    # await session.close()
    #
    assert response.status == expected_answer["status"]
    assert response.json == expected_answer["length"]
