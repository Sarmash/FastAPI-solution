from http import HTTPStatus
from typing import Any

import core.http_exceptions as ex
from db.redis import Cache
from fastapi import APIRouter, Depends, Query, Request, security
from models.filmwork import FilmWork, Forbidden, Unauthorized
from services.filmwork import FilmService, get_film_service
from services.genre import GenreService, get_genre_service
from services.service_base import Filter, Paginator
from fastapi import HTTPException
from core.permissions import permissions, Permissions

router = APIRouter()


@router.get(
    "/{film_id}",
    responses={HTTPStatus.FORBIDDEN.value: {"model": Forbidden},
               HTTPStatus.OK.value: {"model": FilmWork},
               HTTPStatus.UNAUTHORIZED.value: {"model": Unauthorized}},
    summary="Возвращает данные по фильму",
    description="Возвращает название фильма, рейтинг, описание,"
    "жанр(ы), список актеров, сценаристов и режиссеров"
                "в зависимости от уровня доступа пользователя",
)
@Cache()
@permissions(permission=Permissions.User)
async def film_details(
    request: Request,
    film_id: str,
    service: FilmService = Depends(get_film_service),
    token: security.HTTPAuthorizationCredentials = Depends(
        security.HTTPBearer(bearerFormat='Bearer', auto_error=False))
) -> FilmWork:
    """Эндпоинт - /api/v1/films/{film_id} - возвращающий данные по фильму
    С учетом прав доступа пользователя который запрашивает фильм"""

    film = await service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)
    return film


@router.get(
    "/",
    summary="Возвращает список популярных фильмов",
    description="Возвращает список популярных фильмов c названием и рейтингом",
)
@Cache()
@permissions(permission=Permissions.All)
async def related_films(
    request: Request,
    sort: str = Query(
        default="-imdb_rating", description='Sorting by parameter "imdb_rating"'
    ),
    filter_service: Filter = Depends(),
    paginator: Paginator = Depends(),
    service: FilmService = Depends(get_film_service),
    genre_service: GenreService = Depends(get_genre_service),
    token: security.HTTPAuthorizationCredentials = Depends(
        security.HTTPBearer(bearerFormat='Bearer', auto_error=False))
) -> list:
    """Эндпоинт - /api/v1/films/ - возвращающий список фильмов постранично
    - /films/?sort=-imdb_rating&page_size=50&page_number=1 - для запроса по кол-ву фильмов и странице
    - /films?genre=<comedy-uuid>&sort=-imdb_rating - возвращает жанр и популярные фильмы в нём
    - /films?genre=<comedy-uuid> - возвращает похожие фильмы"""
    genre = None
    if filter_service.genre_id:
        genre = await genre_service.get_by_id(filter_service.genre_id)
        if not genre:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=ex.FILM_BY_GENRE_NOT_FOUND,
            )

    films = await service.get_info_films(sort=sort, genre=genre)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)

    films = paginator.pagination(films)

    return films


@router.get(
    "/search/",
    summary="Возвращает список фильмов оп поиску",
    description="Возвращает список фильмов оп поиску c названием и рейтингом",
)
@Cache()
@permissions(permission=Permissions.All)
async def search_films(
    request: Request,
    query: Any = Query(..., description="What movie are we looking for?"),
    paginator: Paginator = Depends(),
    service: FilmService = Depends(get_film_service),
    token: security.HTTPAuthorizationCredentials = Depends(
        security.HTTPBearer(bearerFormat='Bearer', auto_error=False))
) -> list:
    """Эндпоинт - /api/v1/films/search/ - возвращающий страницу поиска фильмов,
    - /search/?query=star&page_size=50&page_number=1 - для запроса по слову "star" """
    films = await service.get_info_films(query=query)

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)

    films = paginator.pagination(films)

    return films
