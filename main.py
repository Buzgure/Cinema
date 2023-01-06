from Domain.book_validator import BookValidator
from Domain.client_card_validator import ClientCardValidator
from Domain.movie_validator import MovieValidator
from Repository.json_repository import GenericRepository
from Service.book_service import BookService
from Service.client_card_service import ClientCardService
from Service.movie_service import MovieService
from Service.search import SearchService
from Service.undo_redo_service import UndoRedoService
from Tests.all_tests import all_tests
from UserInterface.console import Console


def main():
    filename = 'Filme.json'
    filename1 = 'Carduri.json'
    filename2 = 'Rezervari.json'

    undo_redo_service = UndoRedoService()
    movie_repository = GenericRepository(filename)
    movie_validator = MovieValidator()
    book_repository = GenericRepository(filename2)
    movie_service = MovieService(movie_repository, movie_validator,
                                 book_repository, undo_redo_service)
    client_card_repository = GenericRepository(filename1)
    client_card_validator = ClientCardValidator()
    client_card_service = ClientCardService(client_card_repository,
                                            client_card_validator,
                                            undo_redo_service)

    book_validator = BookValidator()
    book_service = BookService(book_repository, movie_repository,
                               client_card_repository, book_validator,
                               undo_redo_service)
    search_service = SearchService(movie_repository, client_card_repository,
                                   book_repository)

    console = Console(movie_service, client_card_service, book_service,
                      search_service, undo_redo_service)
    console.run_console()


if __name__ == '__main__':
    all_tests()
    main()
