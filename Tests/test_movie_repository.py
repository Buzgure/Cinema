from Domain.movie import Movie
from Repository.json_repository import GenericRepository
from utils import clear_file


def test_movie_repository():
    filename = 'test_movies.json'
    clear_file(filename)
    movie_repository = GenericRepository(filename)
    added = Movie('1', 'Spider-Man', 2020, 35, False)
    movie_repository.create(added)
    assert movie_repository.read(added.id_entity) == added
