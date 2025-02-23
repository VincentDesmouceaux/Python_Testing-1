"""
Teste la sauvegarde des clubs dans un fichier JSON, via la classe ClubManager.
"""

import unittest
import os
import json
from app.booking_manager.club_manager import ClubManager


class TestClubManagerSave(unittest.TestCase):
    """
    Classe de tests pour vérifier la bonne mise à jour du fichier JSON
    lorsque l'on modifie un club et qu'on appelle `save_clubs()`.
    """

    def setUp(self):
        """
        Crée un fichier JSON temporaire `test_clubs.json` avec quelques clubs,
        puis instancie un ClubManager pointant vers ce fichier.
        """
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
        """
        Supprime le fichier temporaire une fois les tests terminés,
        afin de ne pas polluer l'environnement.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_clubs_updates_json(self):
        """
        Modifie un club, appelle save_clubs(), puis relit le JSON
        pour vérifier que la modification est bien persistée.
        """
        club = self.manager.find_by_name("Iron Temple")
        self.assertIsNotNone(club, "Le club 'Iron Temple' doit exister.")
        club.points = 2  # Simule une modification

        self.manager.save_clubs()

        # Vérifie la mise à jour en relisant le fichier test_clubs.json
        with open(self.test_file, "r") as f:
            data = json.load(f)

        iron_data = next(
            (c for c in data["clubs"] if c["name"] == "Iron Temple"),
            None
        )
        self.assertIsNotNone(
            iron_data,
            "Les données pour 'Iron Temple' doivent être présentes dans le JSON."
        )
        self.assertEqual(
            iron_data["points"],
            "2",
            "Les points du club doivent avoir été mis à jour dans le JSON."
        )


if __name__ == '__main__':
    unittest.main()
