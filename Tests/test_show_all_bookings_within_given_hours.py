from datetime import datetime

from Domain.book import Book
from Domain.book_validator import BookValidator
from Repository.json_repository import GenericRepository
from Service.book_service import BookService
from Service.undo_redo_service import UndoRedoService
from ViewModels.bookings_date_format import BookingsDateFormat
from utils import clear_file


def test_show_all_bookings_in_interval():
    filename = 'test_show_all_bookings_in_interval.json'
    clear_file(filename)
    bookings_repository = GenericRepository(filename)
    added = Book('1', '1', '1', '20.11.2021 19.00')
    movie_repository = GenericRepository(filename='nume.json')
    card_repository = GenericRepository(filename='nume.json')
    book_validator = BookValidator()
    undo_redo_service = UndoRedoService()
    bookings_service = BookService(bookings_repository, movie_repository,
                                   card_repository, book_validator,
                                   undo_redo_service)
    bookings_repository.create(added)
    second_added = Book('2', '1', '1', '29.11.2021 16.00')
    bookings_repository.create(second_added)
    first_hour = '10.00'
    second_hour = '18.00'
    first_formated = datetime.strptime(first_hour, "%H.%M")
    first_formated_time = first_formated.time()
    second_formated = datetime.strptime(second_hour, "%H.%M")
    second_formated_time = second_formated.time()
    assert bookings_service.show_all_bookings_within_given_hours(
        first_formated_time,
        second_formated_time)[0] == BookingsDateFormat('2', '1', '1')

