import unittest
from app.booking_manager import BookingManager


class TestBookingManager(unittest.TestCase):

    def setUp(self):
        # Instancier un BookingManager avec des JSON de test
        self.manager = BookingManager(
            clubs_file="data/clubs.json",
            competitions_file="data/competitions.json"
        )

    def test_purchase_places_happy_path(self):
        """
        Teste le cas normal :
        - Club a suffisamment de points
        - Compétition a suffisamment de places
        - Moins de 12 places demandées
        """
        success = self.manager.purchase_places(
            "Iron Temple", "Spring Festival", 3)
        self.assertTrue(success, "L'achat de 3 places devrait réussir.")

    def test_purchase_places_too_many_places_requested(self):
        """
        Teste la limite de 12 places : si on essaie d'en prendre 13, ça doit échouer.
        """
        success = self.manager.purchase_places(
            "Iron Temple", "Spring Festival", 13)
        self.assertFalse(
            success, "L'achat de 13 places doit échouer (max 12).")

    # Ajoute d'autres tests pour couvrir :
    # - club sans assez de points
    # - competition full
    # - club ou competition inexistant
    # etc.


if __name__ == "__main__":
    unittest.main()
