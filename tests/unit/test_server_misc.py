"""
Tests complémentaires sur le serveur Flask (app.server).
Couvre des cas particuliers comme /logout non loggué, /book inexistant, etc.
"""

import unittest
from app.server import app


class TestServerMisc(unittest.TestCase):
    """
    Classe de tests pour les routes diverses du serveur
    (logout, book inexistant, purchasePlaces mal formé).
    """

    def setUp(self):
        """
        Active le mode TEST et crée un client de test Flask.
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_logout_not_logged_in(self):
        """
        Vérifie que /logout redirige même si on n'est pas connecté.
        On s'attend à retrouver la page d'accueil.
        """
        response = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Bienvenue sur GUDLFT",
            response.data,
            "On doit se retrouver sur la page d'accueil après logout."
        )

    def test_book_inexisting_competition(self):
        """
        GET /book/<competition>/<club> avec une compétition inexistante
        doit rediriger et flasher un message d'erreur.
        """
        response = self.client.get(
            "/book/FakeCompetition/Iron Temple", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Something went wrong",
            response.data,
            "Un message d'erreur doit être flashé."
        )

    def test_book_inexisting_club(self):
        """
        GET /book/<competition>/<club> avec un club inexistant
        renvoie également un message d'erreur.
        """
        response = self.client.get(
            "/book/Spring Festival/FakeClub", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Something went wrong", response.data)

    def test_purchase_places_value_error(self):
        """
        POST /purchasePlaces avec places='abc' (invalide)
        doit flasher "Le nombre de places est invalide." et rediriger.
        """
        data = {
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "abc"
        }
        response = self.client.post(
            "/purchasePlaces", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Le nombre de places est invalide.",
            response.data
        )


if __name__ == '__main__':
    unittest.main()
