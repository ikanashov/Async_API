from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models.api.v1 import FilmDetail, FilmGenreFilter, FilmQuery, FilmShort, FilmSort, Page

from services.film import FilmService, get_film_service


router = APIRouter()


@router.get(
    '',
    response_model=List[FilmShort],
    summary='Список фильмов',
    description='Список фильмов с пагинацией, фильтрацией по жанрам и сортировкой по рейтингу',
    response_description='uuid, название и рейтинг',
    tags=['Жанры']
)
async def get_all_film(
    genre_filter: FilmGenreFilter = Depends(),
    sort: FilmSort = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmShort]:
    films = await film_service.get_all_film(sort.sort, page.page_size, page.page_number, genre_filter.genre_filter)
    return films


@router.get(
    '/search',
    response_model=List[FilmShort],
    summary='Поиск по фильмам',
    description='Поиск по фильмам (по названию и описанию)',
    response_description='uuid, название и рейтинг'
)
async def search_film(
    query: FilmQuery = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmShort]:
    films = await film_service.search_film(query.query, page.page_size, page.page_number)
    return films


@router.get(
    '/{film_id}',
    response_model=FilmDetail,
    summary='Подробная информация о фильме',
    description='Вывод подробной информации по uuid фильма',
    response_description='uuid, название, рейтинг, описание, жанры, актеры, сценаристы, режисеры'
)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDetail:
    film = await film_service.get_film_by_id(film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film
