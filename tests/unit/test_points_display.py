# tests/unit/test_points_display.py

import unittest
from app.server import app


class TestPointsDisplay(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_points_display_on_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Points Clubs", response.data)

    def test_points_display_on_welcome(self):
        response = self.client.post(
            "/showSummary", data={"email": "admin@irontemple.com"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Points disponibles", response.data)

    def test_clubs_points_route(self):
        """
        Vérifie GET /clubsPoints (200 OK, contient liste des clubs).
        """
        response = self.client.get("/clubsPoints")
        self.assertEqual(response.status_code, 200,
                         "/clubsPoints doit être accessible en GET.")
        self.assertIn(b"Points des Clubs", response.data,
                      "Doit afficher le titre 'Points des Clubs'.")


if __name__ == '__main__':
    unittest.main()
