from dataclasses import Field

from models.base_model import BasicModel


class Person(BasicModel):
    id: str
    full_name: str


class PersonFilmWork(BasicModel):
    uuid: str
    title: str
    imdb_rating: float = 0.0


class PersonOut(BasicModel):
    id: str
    full_name: str
    role: str
    film_ids: list = Field(default_factory=[])