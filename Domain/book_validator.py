from Domain.movie import Movie


class BookValidator:
    def validate(self, movie: Movie):
        if movie.availability is False:
            raise ValueError('Nu se poate efectua o rezervare '
                             'pentru un film ce nu se mai difuzeaza!')
