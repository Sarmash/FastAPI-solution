from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def film_details(genre_id: str,
                       genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    """Эндпоинт - /api/v1/genres/{genre_id} - возвращающий данные по жанру"""

    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return genre
