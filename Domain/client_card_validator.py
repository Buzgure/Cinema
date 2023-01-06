from Domain.client_card import ClientCard


class ClientCardValidator:
    def validate_card(self, card: ClientCard):
        if len(card.CNP) != 13:
            raise ValueError('CNP-ul introdus nu este valid!')
