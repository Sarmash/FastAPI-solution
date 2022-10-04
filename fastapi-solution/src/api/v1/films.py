from http import HTTPStatus
from typing import Any

import core.http_exceptions as ex
from db.redis import cache
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.filmwork import FilmWork
from services.filmwork import FilmService, get_film_service
from services.genre import GenreService, get_genre_service
from services.service_base import Paginator

router = APIRouter()


@router.get("/{film_id}",
            response_model=FilmWork,
            summary="Возвращает данные по фильму",
            description="Возвращает название фильма, рейтинг, описание,"
                        "жанр(ы), список актеров, сценаристов и режиссеров",
            )
@cache
async def film_details(
    request: Request, film_id: str, service: FilmService = Depends(get_film_service)
) -> FilmWork:
    """Эндпоинт - /api/v1/films/{film_id} - возвращающий данные по фильму"""
    film = await service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)
    return film


@router.get("/",
            summary="Возвращает список популярных фильмов",
            description="Возвращает список популярных фильмов c названием и рейтингом",)
@cache
async def related_films(
    request: Request,
    genre: str = Query(None, description="Similar films by genre"),
    sort: str = Query(
        default="-imdb_rating", description='Sorting by parameter "imdb_rating"'
    ),
    paginator: Paginator = Depends(),
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
        sort=sort,
        genre=genre,
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)

    films = paginator.pagination(films)

    return films


@router.get(
    "/search/",
    summary="Возвращает список фильмов оп поиску",
    description="Возвращает список фильмов оп поиску c названием и рейтингом",
)
@cache
async def search_films(
    request: Request,
    query: Any = Query(..., description="What movie are we looking for?"),
    paginator: Paginator = Depends(),
    service: FilmService = Depends(get_film_service),
) -> list:
    """Эндпоинт - /api/v1/films/search/ - возвращающий страницу поиска фильмов,
    - /search/?query=star&page_size=50&page_number=1 - для запроса по слову "star" """
    films = await service.get_info_films(query=query)

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)

    films = paginator.pagination(films)

    return films
