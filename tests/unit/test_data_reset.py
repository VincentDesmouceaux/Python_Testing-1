"""
Teste la fonctionnalité reset_data() des ClubManager et CompetitionManager,
assurant qu'on peut restaurer l'état initial après modifications.
"""

import unittest
import shutil
from app.booking_manager.club_manager import ClubManager
from app.booking_manager.competition_manager import CompetitionManager


class TestDataReset(unittest.TestCase):
    """
    Classe de tests vérifiant que la réinitialisation des données
    (reset_data) fonctionne correctement pour Clubs et Competitions.
    """

    def setUp(self):
        """
        Copie les fichiers *fresh*.json vers clubs.json / competitions.json
        afin de partir d'un état "frais". Puis instancie les managers.
        """
        self.clubs_file = "data/clubs.json"
        self.competitions_file = "data/competitions.json"

        self.fresh_clubs = "data/fresh_clubs.json"
        self.fresh_competitions = "data/fresh_competitions.json"

        shutil.copy(self.fresh_clubs, self.clubs_file)
        shutil.copy(self.fresh_competitions, self.competitions_file)

        self.club_manager = ClubManager(self.clubs_file)
        self.competition_manager = CompetitionManager(self.competitions_file)

    def tearDown(self):
        """
        Optionnel : on pourrait recopier les fresh*.json,
        mais ici on n'y touche pas.
        """
        pass

    def test_reset_data(self):
        """
        Vérifie qu'après avoir modifié un club/compétition,
        on peut appeler reset_data() pour retrouver l'état initial.
        """
        # 1) On modifie un club
        club = self.club_manager.find_by_name("Iron Temple")
        self.assertIsNotNone(club)
        club.points = 0
        self.club_manager.save_clubs()

        # 2) Vérifie que le fichier contient 0 points
        manager_check = ClubManager(self.clubs_file)
        updated_club = manager_check.find_by_name("Iron Temple")
        self.assertEqual(updated_club.points, 0)

        # 3) On appelle reset_data sur le club_manager
        self.club_manager.reset_data(self.fresh_clubs)
        club_after_reset = self.club_manager.find_by_name("Iron Temple")
        self.assertEqual(
            club_after_reset.points,
            34,
            "Le club doit retrouver ses 34 points initiaux."
        )

        # Pareil pour la compétition
        comp = self.competition_manager.find_by_name("Spring Festival")
        self.assertIsNotNone(comp)
        comp.number_of_places = 10
        self.competition_manager.save_competitions()

        manager_check_comp = CompetitionManager(self.competitions_file)
        self.assertEqual(
            manager_check_comp.find_by_name(
                "Spring Festival").number_of_places,
            10
        )

        # Reset
        self.competition_manager.reset_data(self.fresh_competitions)
        comp_after_reset = self.competition_manager.find_by_name(
            "Spring Festival")
        self.assertEqual(
            comp_after_reset.number_of_places,
            39,
            "La compétition doit retrouver ses 39 places initiales."
        )


if __name__ == "__main__":
    unittest.main()
