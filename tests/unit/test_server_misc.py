# tests/unit/test_server_misc.py

import unittest
from app.server import app


class TestServerMisc(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_logout_not_logged_in(self):
        """
        Vérifie que /logout redirige même si on n'est pas connecté.
        """
        response = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bienvenue sur GUDLFT", response.data,
                      "On doit se retrouver sur la page d'accueil.")

    def test_book_inexisting_competition(self):
        """
        GET /book/<competition>/<club> avec competition inexistante => redirige + flash
        """
        response = self.client.get(
            "/book/FakeCompetition/Iron Temple", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Something went wrong", response.data,
                      "Flash message d'erreur attendue.")

    def test_book_inexisting_club(self):
        """
        GET /book/<competition>/<club> avec club inexistant => redirige + flash
        """
        response = self.client.get(
            "/book/Spring Festival/FakeClub", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Something went wrong", response.data)

    def test_purchase_places_value_error(self):
        """
        Envoie un POST /purchasePlaces avec places = 'abc' => ValueError => flash + redirect
        """
        data = {
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "abc"
        }
        response = self.client.post(
            "/purchasePlaces", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Le nombre de places est invalide.", response.data)


if __name__ == '__main__':
    unittest.main()
