import json
from typing import Dict, List, Optional

from models.film import SFilmPersonDetail
from models.interface import AbstractDataStore, AbstractPerson


class Person(AbstractPerson):
    def __init__(self, datastore: AbstractDataStore) -> None:
        self.datastore = datastore

    def set_person_index(self, personindex: str) -> None:
        self.personindex = personindex

    async def get_person_by_id(self, person_id: str) -> Optional[SFilmPersonDetail]:
        person = await self.datastore.get_by_id(self.personindex, person_id)
        if person:
            return SFilmPersonDetail(**person)

    async def get_all_person(
        self,
        sort: str,
        page_size: int, page_number: int
    ) -> Optional[List[SFilmPersonDetail]]:

        persons = await self.datastore.search(
            self.personindex,
            page_size=page_size, page_number=page_number, sort=sort
        )
        persons = [SFilmPersonDetail(**person) for person in persons]
        return persons

    async def search_person(
        self,
        query: str, page_size: int, page_number: int
    ) -> Optional[List[SFilmPersonDetail]]:

        query_body: Dict = {'query': {'match': {'full_name': {'query': query, 'fuzziness': 'AUTO'}}}}
        body = json.dumps(query_body)
        persons = await self.datastore.search(
            self.personindex,
            page_size=page_size, page_number=page_number,
            sort=None, body=body
        )
        persons = [SFilmPersonDetail(**person) for person in persons]
        return persons
