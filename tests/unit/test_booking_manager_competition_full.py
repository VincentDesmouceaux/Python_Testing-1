# tests/unit/test_booking_manager_competition_full.py

import unittest
from app.booking_manager.booking_service import BookingService


class TestBookingManagerCompetitionFull(unittest.TestCase):
    def setUp(self):
        self.service = BookingService(
            clubs_file="data/clubs.json", competitions_file="data/competitions.json")

    def test_purchase_places_competition_full(self):
        competition = self.service.competition_manager.find_by_name(
            "Spring Festival")
        if competition:
            competition.number_of_places = 2  # Forcer une compétition avec peu de places
        success = self.service.purchase_places(
            "Iron Temple", "Spring Festival", 3)
        self.assertFalse(
            success, "L'achat de 3 places doit échouer si la compétition n'a que 2 places disponibles.")


if __name__ == '__main__':
    unittest.main()
