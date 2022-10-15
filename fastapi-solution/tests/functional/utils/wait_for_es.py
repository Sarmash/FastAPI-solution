import elasticsearch
import asyncio

from elasticsearch import Elasticsearch

from backoff import backoff


@backoff()
async def wait_for_es():
    es_client = Elasticsearch(hosts="http://elasticsearch:9200/")
    if not es_client.ping():
        raise elasticsearch.exceptions.ConnectionError


if __name__ == "__main__":
    asyncio.run(wait_for_es())
