from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from services.filmwork import FilmService, get_film_service

# Объект router, в котором регистрируем обработчики.
router = APIRouter()


# Модель ответа API.
class Film(BaseModel):
    id: str
    title: str
    description: str = None
    imdb: float = 0.0
    genre: list = []
    actors: list = []
    writers: list = []
    directors: list = []


# С помощью декоратора регистрируем обработчик film_details.
# Внедряем FilmService с помощью Depends(get_film_service).
@router.get("/{film_id}", response_model=Film)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        # Если фильм не найден, отдаем 404 статус
        # Желательно пользоваться уже определенными HTTP-статусами, которые содержат епит
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    # Перекладываем данные из models.filmwork в Film.
    return Film(
        id=film_id,
        title=film.title,
        description=film.description,
        imdb=film.imdb_rating,
        genre=film.genre,
        actors=film.actors,
        writers=film.writers,
    )


@router.get("/")
async def related_films(
    sort: str = Query(default="-imdb_rating"),
    page_size: int = Query(default=50),
    page_number: int = Query(default=1),
    film_service: FilmService = Depends(get_film_service),
):
    films = await film_service._get_related_films(sort)
    first_number = (page_number - 1) * page_size
    second_number = first_number + page_size
    return films[first_number:second_number]
