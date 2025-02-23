"""
Teste la situation où la compétition n'a pas assez de places (ex: 2) pour satisfaire la demande (3).
"""

import unittest
from app.booking_manager.booking_service import BookingService


class TestBookingManagerCompetitionFull(unittest.TestCase):
    """
    Vérifie que la réservation échoue si la compétition n'a pas assez de places disponibles.
    """

    def setUp(self):
        self.service = BookingService(
            clubs_file="data/clubs.json",
            competitions_file="data/competitions.json"
        )

    def test_purchase_places_competition_full(self):
        """
        Force la compétition 'Spring Festival' à n'avoir que 2 places,
        puis tente d'acheter 3 => doit retourner False.
        """
        competition = self.service.competition_manager.find_by_name(
            "Spring Festival")
        if competition:
            competition.number_of_places = 2
        success = self.service.purchase_places(
            "Iron Temple", "Spring Festival", 3)
        self.assertFalse(
            success,
            "L'achat doit échouer si la compétition n'a que 2 places disponibles."
        )


if __name__ == '__main__':
    unittest.main()
