from datetime import datetime, date

from Domain.add_operation import AddOperation
from Domain.client_card import ClientCard
from Domain.client_card_validator import ClientCardValidator
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Repository.json_repository import GenericRepository
from Service.undo_redo_service import UndoRedoService
from ViewModels.client_name import ClientName
from utils import my_sorted


class ClientCardService:
    def __init__(self,
                 client_card_repository: GenericRepository,
                 client_card_validator: ClientCardValidator,
                 undo_redo_service: UndoRedoService):
        self.client_card_repository = client_card_repository
        self.client_card_validator = client_card_validator
        self.undo_redo_service = undo_redo_service

    def add_card(self,
                 id_card: str,
                 last_name: str,
                 first_name: str,
                 CNP: str,
                 birth_date: str,
                 reg_date: str,
                 loyalty_points: int):
        """
        Adauga un card de client
        :param id_card: id-ul cardului ce va fi adaugat
        :param last_name: Numele clientului
        :param first_name: Prenumele clientului
        :param CNP:CNP-ul clientului
        :param birth_date: Data nasterii
        :param reg_date: Data inregistrarii
        :param loyalty_points: Punctele acumulate de client
        """
        client_card = ClientCard(id_card, last_name, first_name, CNP,
                                 birth_date, reg_date, loyalty_points)
        self.client_card_validator.validate_card(client_card)
        self.client_card_repository.create(client_card)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.client_card_repository, client_card)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_card(self,
                    id_card: str,
                    last_name: str,
                    first_name: str,
                    CNP: str,
                    birth_date: str,
                    reg_date: str,
                    loyalty_points: int):
        """
        Actualizeaza un card de client
        :param id_card:id-ul cardului ce va fi adaugat
        :param last_name: Numele clientului
        :param first_name: Prenumele clientului
        :param CNP:CNP-ul clientului
        :param birth_date: Data nasterii
        :param reg_date: Data inregistrarii
        :param loyalty_points: Punctele acumulate de client
        """
        prev_card = self.client_card_repository.read(id_card)
        client_card = ClientCard(id_card, last_name, first_name, CNP,
                                 birth_date, reg_date, loyalty_points)
        self.client_card_validator.validate_card(client_card)
        self.client_card_repository.update(client_card)
        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.client_card_repository,
                                           client_card, prev_card)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_card(self, id_card: str):
        """
        Sterge cardul cu id-ul
        :param id_card: id-ul cardului ce se va sterge
        """
        card = self.client_card_repository.read(id_card)
        self.client_card_repository.delete(id_card)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.client_card_repository,
                                           card)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> list[ClientCard]:
        """
        Returneaza lista cu carduri
        :return: lista cu carduri
        """
        return self.client_card_repository.read()

    def sorted_client_cards(self):
        """
        Sorteaza cardurile in functie de punctele de loialitate
        :return: lista cu cardurile sortate
        """
        client_card = self.client_card_repository.read()
        cards = [ClientName(card.last_name, card.first_name,
                            card.loyalty_points) for card in client_card]
        sorted_cards = my_sorted(cards, key=lambda x: x.loyalty_points,
                                 reverse=True)
        return sorted_cards

    def raise_loyalty_points(self, value: int,
                             first_date: date,
                             second_date: date) -> None:
        """
        Incrementarea cu value puncte a cardurilor clientilor a caror
        zi de nastere se afla in intervalul(first_date, second_date)
        :param value: valoarea cu care vor fi incrementate punctele
        :param first_date: prima data
        :param second_date: a doua data
        """
        cards = self.client_card_repository.read()
        incremented_cards = [ClientCard(card.id_entity, card.last_name,
                                        card.first_name, card.CNP,
                                        card.birth_date, card.reg_date,
                                        card.loyalty_points + value)
                             for card in cards
                             if first_date <
                             datetime.strptime(card.birth_date,
                                               "%d.%m.%Y").date() <
                             second_date]
        for index in incremented_cards:
            card = ClientCard(index.id_entity, index.last_name,
                              index.first_name, index.CNP,
                              index.birth_date, index.reg_date,
                              index.loyalty_points)
            self.client_card_repository.update(card)
