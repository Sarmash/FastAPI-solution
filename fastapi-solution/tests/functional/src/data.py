import uuid

es_data_films = [
    {
        "id": str(uuid.uuid4()),
        "title": "The Star",
        "imdb_rating": 8.5,
        "description": "New World",
        "genre": ["Action", "Sci-Fi"],
        "actors": [
            {"id": "111", "name": "Ann"},
            {"id": "222", "name": "Bob"},
        ],
        "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
        "director": "Stan",
        "actors_names": ["Ann", "Bob"],
        "writers_names": ["Ben", "Howard"],
    }
    for _ in range(60)
]

data_film_id = [
    {
        "id": "c0142274-dc57-4a3a-a8fe-4c0a229c60f8",
        "title": "The Star",
        "imdb_rating": 9.0,
        "description": "New World",
        "genre": ["Action"],
        "actors": [
            {"id": "111", "name": "Ann"},
            {"id": "222", "name": "Bob"},
        ],
        "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
        "director": "Stan",
        "actors_names": ["Ann", "Bob"],
        "writers_names": ["Ben", "Howard"],
    },
    {
        "id": "c5dc6c27-1c24-4965-8acc-ae7dcd20801c",
        "title": "The Star II",
        "imdb_rating": 8.0,
        "description": "World",
        "genre": ["Sci-Fi"],
        "actors": [
            {"id": "111", "name": "Ann"},
        ],
        "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
        "director": None,
        "actors_names": ["Ann"],
        "writers_names": ["Ben", "Howard"],
    },
    {
        "id": "c0142274-dc57-4a3a-a8fe-4c0a229c60f1",
        "title": "The Star III",
        "imdb_rating": 1.0,
        "description": "New",
        "genre": ["Action", "Sci-Fi"],
        "actors": [
            {"id": "111", "name": "Ann"},
            {"id": "222", "name": "Bob"},
        ],
        "writers": [],
        "director": "Stan",
        "actors_names": ["Ann", "Bob"],
        "writers_names": [],
    },
]

es_data_persons = [
    {"id": "111", "full_name": "Ann"},
    {"id": "222", "full_name": "Bob"},
    {"id": "333", "full_name": "Ben"},
    {"id": "444", "full_name": "Howard"},
]
