from Tests.test_bookings_repository import test_bookings_repository
from Tests.test_client_card_repository import test_client_card_repository
from Tests.test_movie_repository import test_movie_repository
from Tests.test_show_all_bookings_within_given_hours import \
    test_show_all_bookings_in_interval


def all_tests():
    test_movie_repository()
    test_client_card_repository()
    test_bookings_repository()
    test_show_all_bookings_in_interval()
