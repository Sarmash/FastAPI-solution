from typing import Optional, List

from models.base_model import BasicModel


class PersonOut(BasicModel):
    """
    Модель для вывода данных по персоне
    """
    id: str
    full_name: str
    role: str
    film_ids: Optional[List[str]] = []


class FilmWorkOut(BasicModel):
    """
    Модель для вывода фильмов по персоне
    """
    id: str
    title: str
    imdb_rating: Optional[float]
