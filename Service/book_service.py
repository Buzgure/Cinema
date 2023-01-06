import datetime

from Domain.add_operation import AddOperation
from Domain.book import Entity, Book
from Domain.book_validator import BookValidator
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Service.undo_redo_service import UndoRedoService
from ViewModels.bookings_date_format import BookingsDateFormat
from Repository.json_repository import GenericRepository


class BookService:
    def __init__(self,
                 book_repository: GenericRepository,
                 movie_repository: GenericRepository,
                 card_repository: GenericRepository,
                 book_validator: BookValidator,
                 undo_redo_service: UndoRedoService):
        self.book_repository = book_repository
        self.book_validator = book_validator
        self.movie_repository = movie_repository
        self.card_repository = card_repository
        self.undo_redo_service = undo_redo_service

    def add_book(self,
                 id_book: str,
                 id_movie: str,
                 id_card: str,
                 date_time: str):
        """
        Creeaza o rezervare
        :param id_book: id-ul rezervarii
        :param id_movie: id-ul filmului din rezervare
        :param id_card: id-ul cardului de client
        :param date_time: data si ora la care se face rezervarea
        """
        book = Book(id_book, id_movie, id_card, date_time)
        movie = self.movie_repository.read(id_movie)
        self.book_validator.validate(movie)
        self.book_repository.create(book)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.book_repository, book)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_book(self,
                    id_book: str,
                    id_movie: str,
                    id_card: str,
                    date_time: str):
        """
        Actualizeaza o rezervare
        :param id_book: id-ul rezervarii ce se va actualiza
        :param id_movie: id-ul noului film din rezervare
        :param id_card: id-ul noului card de client
        :param date_time: data si ora la care se face noua rezervare
        """
        prev_book = self.book_repository.read(id_book)
        book = Book(id_book, id_movie, id_card, date_time)
        movie = self.movie_repository.read(id_movie)
        self.book_validator.validate(movie)
        self.book_repository.update(book)
        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.book_repository,
                                           book, prev_book)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_book(self, id_book: str):
        """
        Sterge rezervarea
        :param id_book: id-ul rezervarii care se va sterge
        """
        booking = self.book_repository.read(id_book)
        self.book_repository.delete(id_book)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.book_repository,
                                           booking)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> list[Entity]:
        """
        Afiseaza lista cu rezervarile
        :return: lista cu rezervari
        """
        return self.book_repository.read()

    def add_loyalty_points(self, id_booking: str):
        """
        Adauga pe cardul de client punctele acumulate
        """
        booking = self.book_repository.read(id_booking)
        movie = self.movie_repository.read(booking.id_movie)
        movie_price = movie.ticket_price
        points_to_be_added = int(movie_price / 10)
        new_card = self.card_repository.read(booking.id_card)
        new_card.loyalty_points += points_to_be_added
        self.card_repository.update(new_card)

    def show_all_bookings_within_given_hours(self, first_hour: datetime,
                                             second_hour: datetime) -> list:
        """
        Afiseaza rezervarile ce s-au facut intr-un interval dat
        :param first_hour: primul capat al intervalului
        :param second_hour: al doilea capat al intervalului
        :return: lista cu rezervarile din acel interval
        """
        bookings = self.book_repository.read()
        for book in bookings:
            book_date = book.date_time
            book_date_formated = datetime.datetime.strptime(book_date,
                                                            "%d.%m.%Y %H.%M")
            book_date_formated_time = book_date_formated.time()
            book.date_time = book_date_formated_time
        bookings_in_interval = [BookingsDateFormat(book.id_entity,
                                                   book.id_movie, book.id_card)
                                for book in bookings if
                                first_hour < book.date_time < second_hour]
        return bookings_in_interval

    def delete_bookings_within_given_dates(self, first_date: datetime,
                                           second_date: datetime):
        """
        Sterge toate rezervarile ce s-au facut intre 2 date
        :param first_date: Prima data introdusa de utilizator
        :param second_date: A doua data introdusa de utilizator
        :return: Lista cu rezervarile
        """
        bookings = self.book_repository.read()
        for book in bookings:
            book_date = book.date_time
            book_date_formated = datetime.datetime.strptime(book_date,
                                                            "%d.%m.%Y %H.%M")
            book_date_formated_date = book_date_formated.date()
            book.date_time = book_date_formated_date
        bookings_in_interval = [BookingsDateFormat(book.id_entity,
                                                   book.id_movie, book.id_card)
                                for book in bookings if
                                first_date < book.date_time < second_date]
        id_list = []
        for book_in_interval in bookings_in_interval:
            id_list.append(book_in_interval.id_book)
        for index in range(0, len(id_list)):
            self.book_repository.delete(id_list[index])
        return self.book_repository.read()
