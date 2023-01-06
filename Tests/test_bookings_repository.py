from Domain.book import Entity, Book
from Repository.json_repository import GenericRepository
from utils import clear_file


def test_bookings_repository():
    filename = 'test_bookings.json'
    clear_file(filename)
    bookings_repository = GenericRepository(filename)
    added = Book('1', '1', '1', '20-11-2021 19.00')
    bookings_repository.create(added)
    assert bookings_repository.read(added.id_entity) == added
