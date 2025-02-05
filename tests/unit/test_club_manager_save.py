# tests/unit/test_club_manager_save.py

import unittest
import os
import json
from app.booking_manager.club_manager import ClubManager


class TestClubManagerSave(unittest.TestCase):
    def setUp(self):
        # Créez un fichier temporaire de clubs pour les tests
        self.test_file = "data/test_clubs.json"
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
        with open(self.test_file, "w") as f:
            json.dump(clubs_data, f, indent=4)
        self.manager = ClubManager(clubs_file=self.test_file)

    def tearDown(self):
        # Supprimez le fichier temporaire après le test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_clubs_updates_json(self):
        # Modifier les points pour un club
        club = self.manager.find_by_name("Iron Temple")
        self.assertIsNotNone(club, "Le club 'Iron Temple' doit exister.")
        club.points = 2  # On simule une réduction de points

        # Sauvegarder l'état actuel
        self.manager.save_clubs()

        # Relire le fichier pour vérifier la mise à jour
        with open(self.test_file, "r") as f:
            data = json.load(f)
        iron_data = next(
            (c for c in data["clubs"] if c["name"] == "Iron Temple"), None)
        self.assertIsNotNone(
            iron_data, "Les données pour 'Iron Temple' doivent être présentes dans le fichier JSON.")
        self.assertEqual(
            iron_data["points"], "2", "Les points du club doivent être mis à jour dans le fichier JSON.")


if __name__ == '__main__':
    unittest.main()
