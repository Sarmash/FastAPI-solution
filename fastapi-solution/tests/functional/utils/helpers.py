from elasticsearch import AsyncElasticsearch


async def elastic_search_list(
        client: AsyncElasticsearch,
        index: str,
        size: str) -> list[dict]:
    response_elastic = await client.search(index=index, size=size)
    response_elastic = response_elastic['hits']['hits']
    return [item['_source'] for item in response_elastic]
