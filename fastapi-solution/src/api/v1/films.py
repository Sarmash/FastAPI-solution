from http import HTTPStatus
from typing import Any

import core.http_exceptions as ex
from db.redis import cache
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.filmwork import FilmWork
from services.filmwork import FilmService, get_film_service
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get("/{film_id}", response_model=FilmWork)
@cache
async def film_details(
    request: Request, film_id: str, service: FilmService = Depends(get_film_service)
) -> FilmWork:
    """Эндпоинт - /api/v1/films/{film_id} - возвращающий данные по фильму"""
    film = await service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)
    return film


@router.get("/")
@cache
async def related_films(
    request: Request,
    genre: str = Query(None, description="Similar films by genre"),
    sort: str = Query(
        default="-imdb_rating", description='Sorting by parameter "imdb_rating"'
    ),
    page_size: int = Query(default=50, gt=0, description="Number of movies per page."),
    page_number: int = Query(default=1, gt=0, description="Page number."),
    service: FilmService = Depends(get_film_service),
    genre_service: GenreService = Depends(get_genre_service),
) -> list:
    """Эндпоинт - /api/v1/films/ - возвращающий список фильмов постранично
    - /films/?sort=-imdb_rating&page_size=50&page_number=1 - для запроса по кол-ву фильмов и странице
    - /films?genre=<comedy-uuid>&sort=-imdb_rating - возвращает жанр и популярные фильмы в нём
    - /films?genre=<comedy-uuid> - возвращает похожие фильмы"""
    if genre:
        genre = await genre_service.get_by_id(genre)
        if not genre:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=ex.FILM_BY_GENRE_NOT_FOUND,
            )

    films = await service.get_info_films(
        sort=sort, genre=genre, page_size=page_size, page_number=page_number
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)
    return films


@router.get("/search/")
@cache
async def search_films(
    request: Request,
    query: Any = Query(..., description="What movie are we looking for?"),
    page_size: int = Query(default=50, gt=0, description="Number of movies per page."),
    page_number: int = Query(default=1, gt=0, description="Page number."),
    service: FilmService = Depends(get_film_service),
) -> list:
    """Эндпоинт - /api/v1/films/search/ - возвращающий страницу поиска фильмов,
    - /search/?query=star&page_size=50&page_number=1 - для запроса по слову "star" """
    films = await service.get_info_films(
        query=query, page_size=page_size, page_number=page_number
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)
    return films
