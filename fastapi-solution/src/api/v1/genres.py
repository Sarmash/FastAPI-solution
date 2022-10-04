from http import HTTPStatus
from typing import Optional

from db.redis import cache
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.genre import Genre
from services.genre import GenreService, get_genre_service
from services.service_base import Paginator

router = APIRouter()


@router.get("/")
@cache
async def genre_list(
    request: Request,
    service: GenreService = Depends(get_genre_service),
    sort: str = Query(default="asc"),
    paginator: Paginator = Depends(),
) -> list:
    """Эндпоинт - /api/v1/genres/ - возвращающий список жанров постранично"""

    list_genres = await service.get_genres(
        paginator.page_size, paginator.page_number, sort
    )

    if not list_genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="page not found")

    return list_genres


@router.get("/{genre_id}", response_model=Genre)
@cache
async def genre_details(
    request: Request, genre_id: str, service: GenreService = Depends(get_genre_service)
) -> Optional[Genre]:
    """Эндпоинт - /api/v1/genres/{genre_id} - возвращающий данные по жанру"""

    genre = await service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")

    return genre
