from Domain.client_card import ClientCard
from Repository.json_repository import GenericRepository
from utils import clear_file


def test_client_card_repository():
    filename = 'test_client_cards.json'
    clear_file(filename)
    client_card_repository = GenericRepository(filename)
    added = ClientCard('1', 'Nume', 'Prenume', '100000000', '01-01-1990',
                       '20-10-2021', 0)
    client_card_repository.create(added)
    assert client_card_repository.read(added.id_entity) == added
