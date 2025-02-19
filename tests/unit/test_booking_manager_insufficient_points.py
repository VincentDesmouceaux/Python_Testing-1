import unittest
from app.booking_manager.booking_service import BookingService


class TestBookingManagerInsufficientPoints(unittest.TestCase):
    def setUp(self):
        self.service = BookingService(
            clubs_file="data/clubs.json",
            competitions_file="data/competitions.json"
        )

    def test_purchase_places_insufficient_points(self):
        club = self.service.club_manager.find_by_name("Iron Temple")
        if club:
            club.points = 2  # Forcer un club avec peu de points
        success = self.service.purchase_places(
            "Iron Temple", "Spring Festival", 3)
        self.assertFalse(
            success, "L'achat de 3 places doit échouer si le club n'a que 2 points.")


if __name__ == '__main__':
    unittest.main()
