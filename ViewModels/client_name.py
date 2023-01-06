from dataclasses import dataclass


@dataclass
class ClientName:
    last_name: str
    first_name: str
    loyalty_points: int
