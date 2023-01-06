from datetime import datetime

from Domain.movie_validator import MovieValidationError
from Repository.exceptions import DuplicateIdError, NoSuchIdError
from Service.book_service import BookService
from Service.client_card_service import ClientCardService
from Service.movie_service import MovieService
from Service.search import SearchService
from Service.undo_redo_service import UndoRedoService


class Console:
    def __init__(self,
                 movie_service: MovieService,
                 client_card_service: ClientCardService,
                 book_service: BookService,
                 search_service: SearchService,
                 undo_redo_service: UndoRedoService):
        self.movie_service = movie_service
        self.client_card_service = client_card_service
        self.book_service = book_service
        self.search_service = search_service
        self.undo_redo_service = undo_redo_service

    def show_menu(self):
        print('a[mov|card|book] - add film sau card sau rezervare')
        print('u[mov|card|book] - update film sau card sau rezervare')
        print('d[mov|card|book] - delete film sau card sau rezervare')
        print('s[mov|card|book] - showall film sau card sau rezervare')
        print('1. Afișarea tuturor rezervărilor dintr-un interval de ore dat, '
              'indiferent de zi.')
        print('2. Afișarea filmelor ordonate descrescător după numărul de '
              'rezervări.')
        print('3. Afișarea cardurilor client ordonate descrescător după '
              'numărul de puncte de pe card.')
        print('4. Ștergerea tuturor rezervărilor dintr-un anumit interval '
              'de zile.')
        print('5. Incrementarea cu o valoare dată a punctelor'
              ' de pe toate cardurile a căror zi de naștere '
              'se află într-un interval dat.')
        print('s. Căutare filme și clienți. Căutare full text.')
        print('g. Generarea a n entitati de tip Movie.')
        print('sd. Stergerea unui film si a rezervarilor aferente acestuia.')
        print('Undo.')
        print('Redo.')
        print('x. Iesire')

    def run_console(self):
        while True:
            self.show_menu()
            opt = input('Alegeti optiunea: ')

            if opt == 'amov':
                self.handle_add_movie()
            elif opt == 'acard':
                self.handle_add_card()
            elif opt == 'abook':
                self.handle_add_book()
            elif opt == 'umov':
                self.handle_update_movie()
                pass
            elif opt == 'ucard':
                self.handle_update_card()
                pass
            elif opt == 'ubook':
                self.handle_update_book()
                pass
            elif opt == 'dmov':
                self.hanlde_delete_movie()
                pass
            elif opt == 'dcard':
                self.handle_delete_card()
                pass
            elif opt == 'dbook':
                self.handle_delete_book()
                pass
            elif opt == 'smov':
                self.handle_show_all(self.movie_service.get_all())
            elif opt == 'scard':
                self.handle_show_all(self.client_card_service.get_all())
            elif opt == 'sbook':
                self.handle_show_all(self.book_service.get_all())
            elif opt == '1':
                self.handle_show_bookings()
            elif opt == '2':
                self.handle_sort_movies()
            elif opt == '3':
                self.handle_sort_cards()
            elif opt == '4':
                self.handle_delete_bookings_in_interval()
            elif opt == '5':
                self.handle_show_incremented_cards()
            elif opt == 's':
                self.handle_search()
            elif opt == 'g':
                self.handle_generate_movies()
            elif opt == 'sd':
                self.handle_safe_delete()
            elif opt == 'Undo':
                self.undo_redo_service.do_undo()
            elif opt == 'Redo':
                self.undo_redo_service.do_redo()
            elif opt == 'x':
                break
            else:
                print('Comanda invalida')

    def handle_add_movie(self):
        try:
            id = input('Dati id-ul filmului: ')
            title = input('Dati titlul filmului: ')
            year = int(input('Dati anul aparitiei filmului: '))
            ticket_price = float(input('Dati pretul biletului filmului: '))
            availability = input('Filmul se mai difuzeaza in cinema? '
                                 '(True / False) : ')
            if availability == 'True':
                availability = True
            else:
                availability = False

            self.movie_service.add_movie(id, title, year, ticket_price,
                                         availability)
        except MovieValidationError as ve:
            print('Eroare de validare:', ve)
        except DuplicateIdError as de:
            print('Eroare de ID:', de)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_show_all(self, objects):
        for obj in objects:
            print(obj)

    def handle_add_card(self):
        try:
            id_card = input('Dati id-ul card-ului: ')
            last_name = input('Introduceti numele clientului ')
            first_name = input('Introduceti prenumele clientului ')
            CNP = input('Introduceti CNP-ul clientului ')
            birth_date = input('Introduceti data nasterii clientului ')
            reg_date = input('Introduceti data inregistrarii')
            loyalty_points = 0
            self.client_card_service.add_card(id_card,
                                              last_name,
                                              first_name,
                                              CNP,
                                              birth_date,
                                              reg_date,
                                              loyalty_points)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except DuplicateIdError as de:
            print('Eroare de ID:', de)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_add_book(self):
        try:
            id_book = input('Dati id-ul rezervarii: ')
            id_movie = input('Dati id-ul filmului pentru care doriti o '
                             'rezervare: ')
            id_card = input('Dati id-ul cardului de client: ')
            date_time = input('Introduceti data si ora la care doriti sa '
                              'faceti rezervarea: ')
            self.book_service.add_book(id_book, id_movie, id_card, date_time)
            self.book_service.add_loyalty_points(id_book)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except DuplicateIdError as de:
            print('ID Duplicat:', de)
        except Exception as ex:
            print('Eroare:', ex)

    def hanlde_delete_movie(self):
        try:
            id = input('Introduceti id-ul filmului '
                       'pe care vreti sa-l stergeti: ')
            self.movie_service.delete_movie(id)
        except NoSuchIdError as nsie:
            print('Id inexistent: ', nsie)
        except Exception as ex:
            print('Eroare: ', ex)

    def handle_delete_card(self):
        try:
            id = input('Introduceti id-ul cardului '
                       'pe care vreti sa-l stergeti: ')
            self.client_card_service.delete_card(id)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_book(self):
        try:
            id = input('Introduceti id-ul rezervarii '
                       'pe care vreti sa o stergeti: ')
            self.book_service.delete_book(id)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_movie(self):
        try:
            id = input('Dati id-ul filmului care se va actuializa: ')
            new_title = input('Dati noul titlu al filmului: ')
            new_year = int(input('Dati noul an al aparitiei filmului: '))
            new_ticket_price = float(input('Dati noul pret al biletului '
                                           'filmului: '))
            availability = input('Filmul se mai difuzeaza in cinema? '
                                 '(True / False) : ')
            if availability == 'True':
                availability = True
            else:
                availability = False

            self.movie_service.update_movie(id,
                                            new_title,
                                            new_year,
                                            new_ticket_price,
                                            availability)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_card(self):
        try:
            id_card = input('Dati id-ul card-ului ce se va actualiza: ')
            new_last_name = input('Introduceti noul nume al clientului ')
            new_first_name = input('Introduceti noul prenume al clientului ')
            CNP = input('Introduceti CNP-ul clientului ')
            birth_date = input('Introduceti data nasterii clientului ')
            reg_date = input('Introduceti data inregistrarii')
            answer = input('Doriti ca punctele de loialitate '
                           'sa fie resetate? ')
            if answer == 'Da':
                loyalty_points = 0
            else:
                loyalty_points = int(input("Introduceti punctele de "
                                           "loialitate: "))
            self.client_card_service.update_card(id_card,
                                                 new_last_name,
                                                 new_first_name,
                                                 CNP,
                                                 birth_date,
                                                 reg_date,
                                                 loyalty_points)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_book(self):
        try:
            id_book = input('Dati id-ul rezervarii ce se va actualiza: ')
            id_movie = input('Dati noul id al filmului pentru '
                             'care doriti o rezervare: ')
            id_card = input('Dati id-ul cardului de client: ')
            date_time = input('Introduceti data si ora la care '
                              'doriti sa faceti rezervarea: ')
            self.book_service.update_book(id_book, id_movie, id_card,
                                          date_time)
            self.book_service.add_loyalty_points()
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_show_bookings(self):
        first = input("Introduceti primul capat al intervalului: ")
        second = input("Introduceti al doilea capat al intervalului: ")
        first_formated = datetime.strptime(first, "%H.%M")
        first_formated_time = first_formated.time()
        second_formated = datetime.strptime(second, "%H.%M")
        second_formated_time = second_formated.time()
        self.handle_show_all(
            self.book_service.show_all_bookings_within_given_hours(
                first_formated_time,
                second_formated_time))

    def handle_sort_movies(self):
        self.handle_show_all(self.movie_service.find_movies_by_bookings())

    def handle_sort_cards(self):
        self.handle_show_all(self.client_card_service.sorted_client_cards())

    def handle_delete_bookings_in_interval(self):
        first_date = input("Dati prima data: ")
        second_date = input("Dati a doua data: ")
        first_formated = datetime.strptime(first_date, "%d.%m.%Y")
        first_formated_time = first_formated.date()
        second_formated = datetime.strptime(second_date, "%d.%m.%Y")
        second_formated_time = second_formated.date()
        self.book_service. \
            delete_bookings_within_given_dates(first_formated_time,
                                               second_formated_time)

    def handle_generate_movies(self):
        try:
            number = int(input("Cate filme se vor genera: "))
            self.movie_service.generate_random_movie(number)
        except DuplicateIdError as die:
            print("Eroare: ", die)

    def handle_search(self):
        try:
            print('1. Cautare filme')
            print('2. Cautare clienti')
            print('3. Cautare full text')
            option = input('Introduceti tipul de cautare dorit: ')
            if option == '1':
                name = input('Introduceti titlul filmului: ')
                print(self.search_service.movie_search(name))
            elif option == '2':
                name = input('Introduceti numele clientului: ')
                print(self.search_service.client_search(name))
            elif option == '3':
                text = input('Introduceti textul: ')
                print(self.search_service.full_text_search(text))
            else:
                print('Optiune invalida.')
        except Exception as ex:
            print('Eroare:', ex)

    def handle_safe_delete(self):
        to_delete = input('Dati id-ul filmului care se va sterge: ')
        self.movie_service.safe_delete(to_delete)

    def handle_show_incremented_cards(self):
        value = int(input('Introduceti valoarea cu care vor fi incrementate'
                          'punctele cardurilor'))
        first_date = input("Dati prima data: ")
        second_date = input("Dati a doua data: ")
        first_formated = datetime.strptime(first_date, "%d.%m.%Y")
        first_formated_time = first_formated.date()
        second_formated = datetime.strptime(second_date, "%d.%m.%Y")
        second_formated_time = second_formated.date()
        print(self.client_card_service.raise_loyalty_points(
            value,
            first_formated_time,
            second_formated_time))
