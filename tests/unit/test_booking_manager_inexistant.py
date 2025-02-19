import unittest
from app.booking_manager.booking_service import BookingService


class TestBookingManagerInexistant(unittest.TestCase):
    def setUp(self):
        self.service = BookingService(
            clubs_file="data/clubs.json",
            competitions_file="data/competitions.json"
        )

    def test_purchase_places_club_not_found(self):
        success = self.service.purchase_places(
            "NonExistentClub", "Spring Festival", 3)
        self.assertFalse(
            success, "L'achat doit échouer si le club n'existe pas.")

    def test_purchase_places_competition_not_found(self):
        success = self.service.purchase_places(
            "Iron Temple", "NonExistentCompetition", 3)
        self.assertFalse(
            success, "L'achat doit échouer si la compétition n'existe pas.")


if __name__ == '__main__':
    unittest.main()
