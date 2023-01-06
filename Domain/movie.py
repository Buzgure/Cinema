from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Movie(Entity):
    title: str
    year: int
    ticket_price: float
    availability: bool
