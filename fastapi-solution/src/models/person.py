from typing import Optional

from models.base_model import BasicModel


class Person(BasicModel):
    """Модель для участника кинопроизведения"""

    id: str
    full_name: str


class PersonFilmWork(BasicModel):
    """Модель для фильма запрошенного по участнику кинопроизведения"""

    uuid: str
    title: str
    imdb_rating: float = 0.0


class PersonOut(BasicModel):
    """Модель ответа для клинта по запросу о участниках кинопроизведений"""

    id: str
    full_name: str
    role: Optional[str]
    film_ids: Optional[list[str]] = []
