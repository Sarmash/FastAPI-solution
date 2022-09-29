from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get("/")
async def film_details(genre_service: GenreService = Depends(get_genre_service),
                       page: int = Query(default=1, gt=0),
                       page_size: int = Query(default=50, gt=0)) -> list[Genre]:
    """Эндпоинт - /api/v1/genres/ - возвращающий список жанров постранично
    - /api/v1/genres/?page=1&page_size=10 - для запроса по кол-ву жанров и странице"""

    list_genres = await genre_service.get_genres(page_size, page)

    if not list_genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='page not found')

    return list_genres

@router.get("/{genre_id}", response_model=Genre)
async def film_details(genre_id: str,
                       genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    """Эндпоинт - /api/v1/genres/{genre_id} - возвращающий данные по жанру"""

    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return genre
