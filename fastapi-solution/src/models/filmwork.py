from typing import Optional

from models.base_model import BasicModel


class FilmWork(BasicModel):
    id: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str] = None
    genre: list = []
    actors: list = []
    writers: list = []
    directors: Optional[str] = None


class FilmWorkOut(BasicModel):
    id: str
    title: str
    imdb_rating: Optional[float]
