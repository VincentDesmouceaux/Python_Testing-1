# tests/unit/test_static_files.py

import unittest
from app.server import app


class TestStaticFiles(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_css_loaded(self):
        response = self.client.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200,
                         "Le CSS doit être accessible.")
        self.assertTrue(len(response.data) > 0,
                        "Le fichier CSS ne doit pas être vide.")
        self.assertIn(b"body", response.data,
                      "Le CSS doit contenir la règle 'body'.")

    def test_favicon_404(self):
        """
        Vérifie que /favicon.ico renvoie 404 (puisqu'on n'en a pas).
        """
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 404,
                         "On s'attend à un 404 pour /favicon.ico inexistant.")


if __name__ == '__main__':
    unittest.main()
