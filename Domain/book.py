from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Book(Entity):
    id_movie: str
    id_card: str
    date_time: str
