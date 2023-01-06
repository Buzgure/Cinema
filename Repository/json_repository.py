from __future__ import annotations

from typing import Optional, Dict, Type

import jsonpickle

from Domain.entity import Entity
from Repository.exceptions import DuplicateIdError, NoSuchIdError


class GenericRepository:
    def __init__(self, filename):
        #super().__init__()
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[Entity]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects, f))

    def create(self, entity: Entity) -> None:
        """
        Creeaza o entitate
        :param entity: entitatea ce va fi creata
        """

        existing = self.__read_file()
        if self.read(entity.id_entity) is not None:
            raise DuplicateIdError(f'Exista deja o entitate '
                                   f'cu id-ul {entity.id_entity}')

        existing[entity.id_entity] = entity
        self.__write_file(existing)

    def read(self, id_entity=None) -> Type[Optional[Entity] | list[Entity]]:
        """
        Citeste o entitate
        :param id_entity:id-ul entitatii
        :return: - entitatea cu id-ul id_entity, daca id entity != None
                 - lista cu toate entitatile, altfel
        """
        existing = self.__read_file()
        if id_entity:
            if id_entity in existing:
                return existing[id_entity]
            else:
                return None
        return list(existing.values())

    def update(self, entity: Entity) -> None:
        """
        Actualizeaza o entitate
        :param entity: Entitatea cu care se va inlocui cea precedenta
        :return:
        """
        existing = self.__read_file()
        if self.read(entity.id_entity) is None:
            raise NoSuchIdError(f'Nu exista o entitate cu id-ul '
                                f'{entity.id_entity} pe care sa o  actualizam')

        existing[entity.id_entity] = entity
        self.__write_file(existing)

    def delete(self, id_entity: str) -> None:
        """
        Sterge entitatea cu id-ul id_entity
        :param id_entity: id-ul entitatii ce se va sterge
        """
        existing = self.__read_file()
        if self.read(id_entity) is None:
            raise NoSuchIdError(f'Nu exista o entitate cu id-ul '
                                f'{id_entity} pe care sa o stergem')

        del existing[id_entity]
        self.__write_file(existing)
