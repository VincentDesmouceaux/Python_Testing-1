# tests/unit/test_data_reset.py

import unittest
import os
import shutil
from app.booking_manager.club_manager import ClubManager
from app.booking_manager.competition_manager import CompetitionManager


class TestDataReset(unittest.TestCase):

    def setUp(self):
        # Chemins vers vos fichiers "de travail"
        self.clubs_file = "data/clubs.json"
        self.competitions_file = "data/competitions.json"

        # Chemins vers des fichiers "frais" (après clonage)
        self.fresh_clubs = "data/fresh_clubs.json"
        self.fresh_competitions = "data/fresh_competitions.json"

        # On suppose que fresh_clubs.json / fresh_competitions.json existent déjà
        # et contiennent l'état initial (points=34 etc.)

        # S'assurer de partir sur un état connu
        shutil.copy(self.fresh_clubs, self.clubs_file)
        shutil.copy(self.fresh_competitions, self.competitions_file)

        self.club_manager = ClubManager(self.clubs_file)
        self.competition_manager = CompetitionManager(self.competitions_file)

    def tearDown(self):
        # (optionnel) remettre fresh ou faire rien
        pass

    def test_reset_data(self):
        """
        Vérifie qu'après une modification, reset_data() restaure l'état initial.
        """
        # 1) On modifie un club
        club = self.club_manager.find_by_name("Iron Temple")
        self.assertIsNotNone(club)
        club.points = 0  # On simule un usage

        # 2) Sauvegarder
        self.club_manager.save_clubs()

        # 3) Vérifie qu'il a bien 0 points
        manager_check = ClubManager(self.clubs_file)
        updated_club = manager_check.find_by_name("Iron Temple")
        self.assertEqual(updated_club.points, 0)

        # 4) On appelle reset_data
        self.club_manager.reset_data(self.fresh_clubs)

        # 5) Vérifie que c'est revenu à l'état frais (34 par exemple)
        club_after_reset = self.club_manager.find_by_name("Iron Temple")
        self.assertEqual(club_after_reset.points, 34,
                         "Le club doit retrouver ses points initiaux.")

        # Pareil pour les compétitions
        comp = self.competition_manager.find_by_name("Spring Festival")
        self.assertIsNotNone(comp)
        comp.number_of_places = 10
        self.competition_manager.save_competitions()

        # re-load pour vérifier
        manager_check_comp = CompetitionManager(self.competitions_file)
        self.assertEqual(manager_check_comp.find_by_name(
            "Spring Festival").number_of_places, 10)

        # reset
        self.competition_manager.reset_data(self.fresh_competitions)
        comp_after_reset = self.competition_manager.find_by_name(
            "Spring Festival")
        self.assertEqual(comp_after_reset.number_of_places, 39,
                         "La compétition doit retrouver ses places initiales (39).")


if __name__ == "__main__":
    unittest.main()
