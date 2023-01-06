from dataclasses import dataclass


@dataclass
class MoviesWithCounter:
    id_movie: str
    name: str
    bookings: int
