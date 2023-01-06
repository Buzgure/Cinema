from dataclasses import dataclass
from datetime import datetime


@dataclass
class BookingsDateFormat:
    id_book: str
    id_movie: str
    id_card: str