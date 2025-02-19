import unittest
import os
import json
from app.booking_manager.booking_service import BookingService


class TestBookingServicePersistence(unittest.TestCase):
    """
    Teste la persistance des données lors de l'achat de places via BookingService.
    """

    def setUp(self):
        """
        Prépare deux fichiers JSON de test (pour clubs et compétitions)
        afin de ne pas affecter les fichiers de production.
        """
        self.test_clubs_file = "data/test_clubs.json"
        self.test_competitions_file = "data/test_competitions.json"

        clubs_data = {
            "clubs": [
                {
                    "id": "1",
                    "name": "Simply Lift",
                    "email": "john@simplylift.co",
                    "points": "13"
                },
                {
                    "id": "2",
                    "name": "Iron Temple",
                    "email": "admin@irontemple.com",
                    "points": "4"
                },
                {
                    "id": "3",
                    "name": "She Lifts",
                    "email": "kate@shelifts.co.uk",
                    "points": "12"
                }
            ]
        }

        competitions_data = {
            "competitions": [
                {
                    "name": "Spring Festival",
                    "date": "2020-03-27 10:00:00",
                    "numberOfPlaces": "25"
                },
                {
                    "name": "Fall Classic",
                    "date": "2020-10-22 13:30:00",
                    "numberOfPlaces": "13"
                }
            ]
        }

        # Écrit les données JSON dans des fichiers temporaires
        with open(self.test_clubs_file, "w") as f:
            json.dump(clubs_data, f, indent=4)
        with open(self.test_competitions_file, "w") as f:
            json.dump(competitions_data, f, indent=4)

        # Instancie BookingService avec ces fichiers de test
        self.service = BookingService(
            clubs_file=self.test_clubs_file,
            competitions_file=self.test_competitions_file
        )

    def tearDown(self):
        """
        Supprime les fichiers temporaires pour ne pas polluer l'environnement.
        """
        if os.path.exists(self.test_clubs_file):
            os.remove(self.test_clubs_file)
        if os.path.exists(self.test_competitions_file):
            os.remove(self.test_competitions_file)

    def test_booking_service_persistence(self):
        """
        Vérifie qu'après une réservation de 3 places pour "Iron Temple" dans "Spring Festival" :
        - Le nombre de points du club est mis à jour (4 - 3 = 1).
        - Le nombre de places dans la compétition est mis à jour (25 - 3 = 22).
        - Les modifications sont bien persistées dans les fichiers JSON.
        """
        success = self.service.purchase_places(
            "Iron Temple", "Spring Festival", 3)
        self.assertTrue(success, "La réservation devrait réussir.")

        # Vérification du fichier JSON des clubs
        with open(self.test_clubs_file, "r") as f:
            clubs_data = json.load(f)

        iron_club = next(
            (club for club in clubs_data["clubs"]
             if club["name"] == "Iron Temple"),
            None
        )
        self.assertIsNotNone(
            iron_club, "Les données du club 'Iron Temple' doivent être présentes.")
        self.assertEqual(
            iron_club["points"], "1", "Les points doivent être mis à jour (4 - 3 = 1).")

        # Vérification du fichier JSON des compétitions
        with open(self.test_competitions_file, "r") as f:
            competitions_data = json.load(f)

        spring_comp = next(
            (comp for comp in competitions_data["competitions"]
             if comp["name"] == "Spring Festival"),
            None
        )
        self.assertIsNotNone(
            spring_comp, "Les données de 'Spring Festival' doivent être présentes.")
        self.assertEqual(spring_comp["numberOfPlaces"], "22",
                         "Les places doivent être mises à jour (25 - 3 = 22).")


if __name__ == '__main__':
    unittest.main()
