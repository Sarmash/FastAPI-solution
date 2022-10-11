import asyncio
import json

from elasticsearch import AsyncElasticsearch

person_data = [{"id": '111', "full_name": "Ann"},
               {"id": "222", "full_name": "Bob"},
               {"id": '333', "full_name": 'Ben'},
               {"id": '444', "full_name": 'Howard'}]


async def gen_data_persons():

    es_data_persons = [{"id": '111', "full_name": "Ann"},
                       {"id": "222", "full_name": "Bob"},
                       {"id": '333', "full_name": 'Ben'},
                       {"id": '444', "full_name": 'Howard'}]

    bulk_query_perons = []
    for row in es_data_persons:
        bulk_query_perons.extend([
            json.dumps({'index': {"_index": "persons",
                                  "_id": row["id"]}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query_perons) + '\n'

    es_client = AsyncElasticsearch(hosts=['http://elasticsearch:9200'])
    response = await es_client.bulk(str_query, refresh=True)
    await es_client.close()
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')


if __name__ == "__main__":
    asyncio.run(gen_data_persons())
