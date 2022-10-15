import asyncio

import elasticsearch
from backoff import backoff
from elasticsearch import Elasticsearch


@backoff()
async def wait_for_es():
    es_client = Elasticsearch(hosts="http://elasticsearch:9200/")
    if not es_client.ping():
        raise elasticsearch.exceptions.ConnectionError


if __name__ == "__main__":
    asyncio.run(wait_for_es())
