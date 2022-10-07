import json
from typing import List


def get_es_bulk_query(data: List[dict], index: str, id: str):
    bulk_query = []
    for row in data:
        bulk_query.extend(
            [json.dumps({"index": {"_index": index, "_id": row[id]}}), json.dumps(row)]
        )

    return bulk_query
