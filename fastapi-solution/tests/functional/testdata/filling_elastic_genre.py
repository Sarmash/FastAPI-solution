import asyncio

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

GENRES = (
    {"genre": "Drama", "id": "1cacff68-643e-4ddd-8f57-84b62538081a"},
    {"genre": "Adventure", "id": "120a21cf-9097-479e-904a-13dd7198c1dd"},
    {"genre": "Animation", "id": "6a0a479b-cfec-41ac-b520-41b2b007b611"},
)


async def genres_index_filling():
    """Функция заполнения индекса жанров тестовыми данными"""

    genres = [
        {"genre": "Sci-Fi", "id": "6c162475-c7ed-4461-9184-001ef3d9f26e"},
        {"genre": "Action", "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"},
        {"genre": "Comedy", "id": "5373d043-3f41-4ea8-9947-4b746c601bbd"},
        {"genre": "Music", "id": "56b541ab-4d66-4021-8708-397762bff2d4"},
        {"genre": "Documentary", "id": "6d141ad2-d407-4252-bda4-95590aaf062a"},
        {"genre": "Biography", "id": "ca124c76-9760-4406-bfa0-409b1e38d200"},
        {"genre": "Crime", "id": "63c24835-34d3-4279-8d81-3c5f4ddb0cdc"},
        {"genre": "Mystery", "id": "ca88141b-a6b4-450d-bbc3-efa940e4953f"},
        {"genre": "Drama", "id": "1cacff68-643e-4ddd-8f57-84b62538081a"},
        {"genre": "Adventure", "id": "120a21cf-9097-479e-904a-13dd7198c1dd"},
        {"genre": "Animation", "id": "6a0a479b-cfec-41ac-b520-41b2b007b611"},
        {"genre": "Family", "id": "55c723c1-6d90-4a04-a44b-e9792040251a"},
        {"genre": "Fantasy", "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd"},
        {"genre": "Romance", "id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5"},
        {"genre": "Western", "id": "0b105f87-e0a5-45dc-8ce7-f8632088f390"},
        {"genre": "Short", "id": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395"},
        {"genre": "Thriller", "id": "526769d7-df18-4661-9aa6-49ed24e9dfd8"},
        {"genre": "Game-Show", "id": "fb58fd7f-7afd-447f-b833-e51e45e2a778"},
        {"genre": "Reality-TV", "id": "e508c1c8-24c0-4136-80b4-340c4befb190"},
        {"genre": "Musical", "id": "9c91a5b2-eb70-4889-8581-ebe427370edd"},
        {"genre": "History", "id": "eb7212a7-dd10-4552-bf7b-7a505a8c0b95"},
        {"genre": "War", "id": "c020dab2-e9bd-4758-95ca-dbe363462173"},
        {"genre": "Horror", "id": "f39d7b6d-aef2-40b1-aaf0-cf05e7048011"},
        {"genre": "Sport", "id": "2f89e116-4827-4ff4-853c-b6e058f71e31"},
        {"genre": "News", "id": "f24fd632-b1a5-4273-a835-0119bd12f829"},
        {"genre": "Talk-Show", "id": "31cabbb5-6389-45c6-9b48-f7f173f6c40f"},
    ]
    client = AsyncElasticsearch(hosts=["http://elasticsearch:9200"])
    genres_for_bulk = [
        {
            "_index": "genres",
            "_id": genre["id"],
            "_type": "_doc",
            "genre": genre["genre"],
            "id": genre["id"],
        }
        for genre in genres
    ]
    await async_bulk(client, genres_for_bulk)
    await client.close()


if __name__ == "__main__":
    asyncio.run(genres_index_filling())
