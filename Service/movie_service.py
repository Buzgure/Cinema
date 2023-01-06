from random import randint
import random
import string

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Service.undo_redo_service import UndoRedoService
from ViewModels.movies_with_counter import MoviesWithCounter
from Domain.movie import Movie
from Domain.movie_validator import MovieValidator
from Repository.json_repository import GenericRepository
from utils import my_sorted


class MovieService:
    def __init__(self,
                 movie_repository: GenericRepository,
                 movie_validator: MovieValidator,
                 bookings_repository: GenericRepository,
                 undo_redo_service: UndoRedoService):
        self.movie_repository = movie_repository
        self.movie_validator = movie_validator
        self.bookings_repository = bookings_repository
        self.undo_redo_service = undo_redo_service

    def add_movie(self,
                  id_movie: str,
                  title: str,
                  year: int,
                  ticket_price: float,
                  availability: bool):
        """
        Adauga un film
        :param id_movie: id-ul filmului
        :param title: Titlul filmului
        :param year: Anul aparitiei filmului
        :param ticket_price: Pretul biletului
        :param availability: Filmul mai ruleaza in cinema sau nu
        """
        movie = Movie(id_movie, title, year, ticket_price, availability)
        self.movie_validator.validate_movie(movie)
        self.movie_repository.create(movie)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.movie_repository, movie)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_movie(self,
                     id_movie: str,
                     title: str,
                     year: int,
                     ticket_price: float,
                     availability: bool):
        """
        Actualizeaza un film
        :param id_movie:id-ul filmului
        :param title: Titlul filmului
        :param year: Anul aparitiei filmului
        :param ticket_price: Pretul biletului
        :param availability: Filmul mai ruleaza in cinema sau nu
        """
        prev_movie = self.movie_repository.read(id_movie)
        movie = Movie(id_movie, title, year, ticket_price, availability)
        self.movie_validator.validate_movie(movie)
        self.movie_repository.update(movie)
        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.movie_repository,
                                           movie, prev_movie)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_movie(self, id_movie: str):
        """
        Sterge filmul cu id-ul id_movie
        :param id_movie:id-ul filmului ce va fi sters
        """
        movie = self.movie_repository.read(id_movie)
        self.movie_repository.delete(id_movie)

        self.undo_redo_service.clear_redo()
        deleted_operation = DeleteOperation(self.movie_repository,
                                            movie)
        self.undo_redo_service.add_to_undo(deleted_operation)

    def get_all(self) -> list[Movie]:
        """
        Afiseaza lista cu toate filmele
        :return: lista cu toate filmele
        """
        return self.movie_repository.read()

    def find_movies_by_bookings(self):
        """
        Afiseaza o loista cu filmele ordonate dupa numarul de rezervari
        facute pentru acesta
        :return: lista ordonata
        """
        movies = self.movie_repository.read()

        counter = {}
        bookings = self.bookings_repository.read()
        for booking in bookings:
            booking_id_movie = booking.id_movie
            if booking_id_movie in counter:
                counter[booking_id_movie] += 1
            else:
                counter[booking_id_movie] = 1
        for movie in movies:
            id_movie = movie.id_entity
            if id_movie not in counter:
                counter[id_movie] = 0
        movies_with_counter = [MoviesWithCounter(movie.id_entity, movie.title,
                                                 counter[movie.id_entity]) for
                               movie in movies]
        sorted_movies_with_counter = my_sorted(movies_with_counter,
                                               key=lambda x: x.bookings,
                                               reverse=True)
        return sorted_movies_with_counter

    def generate_random_movie(self, number: int) -> None:
        """
        Genereaza un numar dat de entitati.
        :param number:Numarul dorit de generari
        :return:None
        """
        possible_movie_availability = [True, False]
        random_list = random.sample(range(0, number), number)
        for index in range(0, number):
            id_movie = str(random_list[index])
            movie_title = ''.join(random.choices(string.ascii_lowercase +
                                                 string.ascii_uppercase +
                                                 string.digits))
            year = randint(1900, 2021)
            ticket_price = random.uniform(20.0, 60.0)
            movie_availability = random.choice(possible_movie_availability)
            movie = Movie(id_movie, movie_title, year, ticket_price,
                          movie_availability)
            self.movie_validator.validate_movie(movie)
            self.movie_repository.create(movie)

    def safe_delete(self, to_delete: str):
        """
        Sterge un film, si rezervarea aferenta acestuia
        :param to_delete: id-ul filmului care se va sterge
        :return:
        """
        bookings = self.bookings_repository.read()
        self.undo_redo_service.clear_redo()
        for booking in bookings:
            if booking.id_movie == to_delete:
                booking_to_delete = self.bookings_repository.read(
                    booking.id_entity)
                delete_operation = DeleteOperation(self.bookings_repository,
                                                   booking_to_delete)
                self.undo_redo_service.add_to_undo(delete_operation)
                self.bookings_repository.delete(booking.id_entity)
        movie_to_delete = self.movie_repository.read(to_delete)
        self.movie_repository.delete(to_delete)
        delete_operation = DeleteOperation(self.movie_repository,
                                           movie_to_delete)
        self.undo_redo_service.add_to_undo(delete_operation)
