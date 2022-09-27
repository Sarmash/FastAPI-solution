from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get("/")
async def film_details(genre_service: GenreService = Depends(get_genre_service),
                       page: int = Query(default=1),
                       page_size: int = Query(default=50)) -> list[Genre]:
    """Эндпоинт - /api/v1/genres/ - возвращающий список жанров"""

    list_genres = await genre_service.get_genres(page, page_size)

    if not list_genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='page not found')

    return list_genres
