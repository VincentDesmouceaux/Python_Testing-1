import unittest
from app.server import app


class TestPointsDisplay(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_points_display_on_index(self):
        """Vérifie que la page d'accueil contient un indice sur l'affichage des points."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # Vérifie qu'un lien "Points Clubs" est présent
        self.assertIn(b"Points Clubs", response.data)

    def test_points_display_on_welcome(self):
        """Vérifie que la page welcome affiche les points après connexion."""
        response = self.client.post(
            "/showSummary", data={"email": "admin@irontemple.com"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Points disponibles", response.data)


if __name__ == '__main__':
    unittest.main()
