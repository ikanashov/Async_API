from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models.api.v1 import FilmPersonDetail, FilmPersonQuery, FilmPersonSort, FilmShort, Page

from services.film import FilmService, get_film_service


router = APIRouter()


@router.get(
    '',
    response_model=List[FilmPersonDetail],
    summary='Список участников съемочных групп',
    description='Список участников съемочных групп с пагинацией и сортировкой по имени',
    response_description='uuid, имя, профессия и список фильмов'
)
async def get_all_person(
    sort: FilmPersonSort = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmPersonDetail]:
    persons = await film_service.get_all_person(sort.sort, page.page_size, page.page_number)
    return persons


@router.get(
    '/search',
    response_model=List[FilmPersonDetail],
    summary='Поиск по участникам',
    description='Поиск по имени участника',
    response_description='uuid, имя, профессия и список фильмов'
)
async def search_person(
    query: FilmPersonQuery = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmPersonDetail]:
    persons = await film_service.search_person(query.query, page.page_size, page.page_number)
    return persons


@router.get(
    '/{person_id}',
    response_model=FilmPersonDetail,
    summary='Информация о персоне',
    description='Вывод подробной информации о конкретном человеке',
    response_description='uuid, имя, профессия и список фильмов'
)
async def person_details(person_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmPersonDetail:
    person = await film_service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return FilmPersonDetail(**person.dict(by_alias=True))


@router.get(
    '/{person_id}/film',
    response_model=List[FilmShort],
    deprecated=True,
    summary='Фильмы персоны (устаревший)',
    description='Вывод инормации о фильмах конретного человека, нежелательно к использованию',
    response_description='uuid, название фильма, рейтинг'
)
async def films_by_person(person_id: str, film_service: FilmService = Depends(get_film_service)) -> List[FilmShort]:
    person = await film_service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    films = [await film_service.get_film_by_id(film_id) for film_id in person.filmids if film_id is not None]
    return films
