import random
import string
from random import randint

from Domain.movie import Movie
from Domain.movie_validator import MovieValidator
from Repository.json_repository import GenericRepository


class MovieGenerator:
    def __init__(self,
                 movie_repository: GenericRepository,
                 movie_validator: MovieValidator):
        self.movie_repository = movie_repository
        self.movie_validator = movie_validator

    def generate_random_movie(self, number: int):
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

    def get_all(self) -> list[Movie]:
        return self.movie_repository.read()
