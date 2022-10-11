import uuid

es_data_films = [
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

es_data_persons = [
    {"id": "111", "full_name": "Ann"},
    {"id": "222", "full_name": "Bob"},
    {"id": "333", "full_name": "Ben"},
    {"id": "444", "full_name": "Howard"},
]
