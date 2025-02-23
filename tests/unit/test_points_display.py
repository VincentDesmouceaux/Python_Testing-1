"""
Tests unitaires ciblant l'affichage des points :
 - sur la page d'accueil (lien Points Clubs)
 - sur la page welcome (points disponibles)
 - sur la route /clubsPoints
"""

import unittest
from app.server import app


class TestPointsDisplay(unittest.TestCase):
    """
    Classe de tests axée sur l'affichage des points et la présence
    de la route /clubsPoints.
    """

    def setUp(self):
        """
        Initialise le mode TEST et le client Flask.
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_points_display_on_index(self):
        """
        Vérifie que la page d'accueil (GET /) renvoie un code 200
        et contient le lien "Points Clubs".
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Points Clubs", response.data)

    def test_points_display_on_welcome(self):
        """
        Vérifie que, après une connexion POST /showSummary,
        la page welcome contient "Points disponibles".
        """
        response = self.client.post(
            "/showSummary",
            data={"email": "admin@irontemple.com"},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Points disponibles", response.data)

    def test_clubs_points_route(self):
        """
        Vérifie que GET /clubsPoints renvoie un code 200
        et contient le titre "Points des Clubs".
        """
        response = self.client.get("/clubsPoints")
        self.assertEqual(
            response.status_code,
            200,
            "/clubsPoints doit être accessible en GET."
        )
        self.assertIn(
            b"Points des Clubs",
            response.data,
            "Le titre 'Points des Clubs' doit apparaître."
        )


if __name__ == '__main__':
    unittest.main()
