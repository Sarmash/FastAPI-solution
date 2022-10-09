import json

import pytest

from ..settings import test_settings


@pytest.mark.asyncio
async def test_films_search_200(session_client, es_client, redis_client):

    response_api = await session_client.get(f"{test_settings.service_url}"
                                            f"{test_settings.search_films_endpoint}"
                                            f"?query=lucas")
    assert response_api.status == 200
    response_api = await response_api.json()
