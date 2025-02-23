"""
Teste la persistance de la réservation via BookingService (clubs.json, competitions.json).
"""

import unittest
import os
import json
from app.booking_manager.booking_service import BookingService


class TestBookingServicePersistence(unittest.TestCase):
    """
    Vérifie que l'achat de places modifie correctement les fichiers JSON
    (clubs et compétitions), en décrémentant les points du club et
    le nombre de places de la compétition.
    """

    def setUp(self):
        """
        Crée deux fichiers JSON temporaires pour clubs et competitions,
        afin d'éviter d'impacter les fichiers de production.
        """
        self.test_clubs_file = "data/test_clubs.json"
        self.test_competitions_file = "data/test_competitions.json"

        clubs_data = {
            "clubs": [
                {"id": "1", "name": "Simply Lift",
                    "email": "john@simplylift.co", "points": "13"},
                {"id": "2", "name": "Iron Temple",
                    "email": "admin@irontemple.com", "points": "4"},
                {"id": "3", "name": "She Lifts",
                    "email": "kate@shelifts.co.uk", "points": "12"}
            ]
        }

        competitions_data = {
            "competitions": [
                {"name": "Spring Festival", "date": "2020-03-27 10:00:00",
                    "numberOfPlaces": "25"},
                {"name": "Fall Classic", "date": "2020-10-22 13:30:00",
                    "numberOfPlaces": "13"}
            ]
        }

        with open(self.test_clubs_file, "w") as f:
            json.dump(clubs_data, f, indent=4)
        with open(self.test_competitions_file, "w") as f:
            json.dump(competitions_data, f, indent=4)

        self.service = BookingService(
            clubs_file=self.test_clubs_file,
            competitions_file=self.test_competitions_file
        )

    def tearDown(self):
        """
        Supprime les fichiers temporaires à la fin du test.
        """
        if os.path.exists(self.test_clubs_file):
            os.remove(self.test_clubs_file)
        if os.path.exists(self.test_competitions_file):
            os.remove(self.test_competitions_file)

    def test_booking_service_persistence(self):
        """
        Vérifie qu'après un achat de 3 places par 'Iron Temple' dans 'Spring Festival':
         - Les points du club passent de 4 à 1
         - Les places de la compétition passent de 25 à 22
         - Le tout est bien sauvegardé dans les fichiers JSON
        """
        success = self.service.purchase_places(
            "Iron Temple", "Spring Festival", 3)
        self.assertTrue(
            success, "La réservation devrait réussir (club a 4 points, compet a 25 places).")

        # Vérification du fichier clubs JSON
        with open(self.test_clubs_file, "r") as f:
            clubs_data = json.load(f)

        iron_club = next(
            (club for club in clubs_data["clubs"]
             if club["name"] == "Iron Temple"),
            None
        )
        self.assertIsNotNone(
            iron_club, "Le club 'Iron Temple' doit exister dans le JSON.")
        self.assertEqual(
            iron_club["points"],
            "1",
            "Les points doivent avoir été décrémentés (4 - 3 = 1)."
        )

        # Vérification du fichier competitions JSON
        with open(self.test_competitions_file, "r") as f:
            competitions_data = json.load(f)

        spring_comp = next(
            (comp for comp in competitions_data["competitions"]
             if comp["name"] == "Spring Festival"),
            None
        )
        self.assertIsNotNone(
            spring_comp, "La compétition 'Spring Festival' doit exister dans le JSON.")
        self.assertEqual(
            spring_comp["numberOfPlaces"],
            "22",
            "Le nombre de places doit avoir été décrémenté (25 - 3 = 22)."
        )


if __name__ == '__main__':
    unittest.main()
