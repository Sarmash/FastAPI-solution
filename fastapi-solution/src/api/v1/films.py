from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from models.filmwork import FilmWork
from services.filmwork import FilmService, get_film_service

router = APIRouter()


async def pagination(films: list, page_size: int, page_number: int) -> list:
    first_number = (page_number - 1) * page_size
    if first_number >= len(films) or len(films) == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="page not found")
    second_number = first_number + page_size
    return films[first_number:second_number]


@router.get("/{film_id}", response_model=FilmWork)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmWork:
    """Эндпоинт - /api/v1/films/{film_id} - возвращающий данные по фильму"""
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film


@router.get("/")
async def related_films(
    sort: str = Query(
        default="-imdb_rating", description='Sorting by parameter "imdb_rating"'
    ),
    page_size: int = Query(default=50, gt=0, description="Number of movies per page."),
    page_number: int = Query(default=1, gt=0, description="Page number."),
    film_service: FilmService = Depends(get_film_service),
) -> list:
    """Эндпоинт - /api/v1/films/ - возвращающий список фильмов постранично
    - /films/?sort=-imdb_rating&page_size=50&page_number=1 - для запроса по кол-ву фильмов и странице"""
    films_list = await film_service.get_info_films()
    value = sort[1:] if sort[0] == "-" else sort
    reverse = True if value == sort[1:] else False
    films = sorted(
        films_list,
        key=lambda x: x.__dict__[value] if isinstance(x.__dict__[value], float) else 0,
        reverse=reverse,
    )
    films = await pagination(films, page_size, page_number)
    return films


@router.get("/search/")
async def source_films(
    query: Any = Query(..., description="What movie are we looking for?"),
    page_size: int = Query(default=50, gt=0, description="Number of movies per page."),
    page_number: int = Query(default=1, gt=0, description="Page number."),
    film_service: FilmService = Depends(get_film_service),
) -> list:
    """Эндпоинт - /api/v1/films/search/ - возвращающий страницу поиска фильмов,
    - /search/?query=star&page_size=50&page_number=1 - для запроса по слову "star" """
    films_list = await film_service.search_films(query)
    films = await pagination(films_list, page_size, page_number)
    return films
