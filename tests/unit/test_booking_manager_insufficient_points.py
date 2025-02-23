"""
Teste le scénario où le club n'a pas assez de points pour acheter le nombre de places souhaité.
"""

import unittest
from app.booking_manager.booking_service import BookingService


class TestBookingManagerInsufficientPoints(unittest.TestCase):
    """
    Vérifie que la réservation échoue quand le club ne dispose pas
    d'assez de points.
    """

    def setUp(self):
        """
        Utilise les fichiers clubs.json et competitions.json réels (ou tests)
        pour initialiser le service.
        """
        self.service = BookingService(
            clubs_file="data/clubs.json",
            competitions_file="data/competitions.json"
        )

    def test_purchase_places_insufficient_points(self):
        """
        Force le club 'Iron Temple' à n'avoir que 2 points,
        et tente d'acheter 3 places => doit échouer (return False).
        """
        club = self.service.club_manager.find_by_name("Iron Temple")
        if club:
            club.points = 2
        success = self.service.purchase_places(
            "Iron Temple", "Spring Festival", 3)
        self.assertFalse(
            success,
            "L'achat de 3 places doit échouer si le club n'a que 2 points."
        )


if __name__ == '__main__':
    unittest.main()
