from Repository.json_repository import GenericRepository


class SearchService:
    def __init__(self,
                 movie_repository: GenericRepository,
                 card_repository: GenericRepository,
                 bookings_repository: GenericRepository):
        self.movie_repository = movie_repository
        self.card_repository = card_repository
        self.bookings_repository = bookings_repository

    def movie_search(self, name: str):
        """
        Cauta numele filmului in repository
        :param name: Numele introdus de la tastatura
        :return: Filmul cu numele name
        """
        found = []
        movies = self.movie_repository.read()
        for movie in movies:
            if name in movie.title:
                found.append(movie)
        return found

    def client_search(self, name: str):
        """
        Cauta numele clientului in client_card_repository
        :param name: Numele introdus
        :return: Cardul creat pe numele name
        """
        found = []
        cards = self.card_repository.read()
        for card in cards:
            if name in card.first_name or name in card.last_name:
                found.append(card)
        return found

    def full_text_search(self, text: str):
        """
        Cauta un string in toate repository-urile
        :param text: Textul introdus
        :return: Entitatea ce contine textul text
        """
        found = []
        movies = self.movie_repository.read()
        cards = self.card_repository.read()
        bookings = self.bookings_repository.read()
        for movie in movies:
            if text in movie.title or text in str(movie.year) or text in \
                    str(movie.ticket_price) \
                    or text in str(movie.availability):
                found.append(movie)
        for card in cards:
            if text in card.last_name or text in card.last_name or text in \
                    card.CNP \
                    or text in card.birth_date or text in \
                    text in card.reg_date \
                    or text in str(card.loyalty_points):
                found.append(card)
        for booking in bookings:
            if text in booking.id_movie or text in booking.id_card or text in \
                    booking.date_time:
                found.append(booking)
        return found
