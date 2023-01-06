from dataclasses import dataclass
from Domain.entity import Entity


@dataclass
class ClientCard(Entity):
    last_name: str
    first_name: str
    CNP: str
    birth_date: str
    reg_date: str
    loyalty_points: int
