import time

from elasticsearch import Elasticsearch

if __name__ == "__main__":
    es_client = Elasticsearch(hosts="http://elasticsearch:9200/")
    while True:
        if es_client.ping():
            break
        time.sleep(5)
