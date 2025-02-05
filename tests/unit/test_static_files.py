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
                         "Le CSS devrait être accessible et retourner un code 200.")
        self.assertTrue(len(response.data) > 0,
                        "Le fichier CSS ne doit pas être vide.")
        self.assertIn(b"body", response.data,
                      "Le CSS doit contenir la règle 'body'.")


if __name__ == '__main__':
    unittest.main()
