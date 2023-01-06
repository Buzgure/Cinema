from Domain.movie import Movie

class MovieValidationError(Exception):
    pass

class MovieValidator:
    def validate_movie(self, movie: Movie):
        if movie.ticket_price <= 0:
            raise MovieValidationError('Pretul trebuie sa fie pozitiv!')
        valid_instances = [True, False]
        if movie.availability not in valid_instances:
            raise MovieValidationError('Raspunsul trebuie '
                                       'sa fie de forma True / False!')
