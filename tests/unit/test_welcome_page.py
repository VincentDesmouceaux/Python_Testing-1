# tests/unit/test_welcome_page.py

import unittest
from app.server import app


class TestWelcomePage(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_show_summary_unknown_email_redirects(self):
        response = self.client.post(
            '/showSummary', data={'email': 'unknown@example.com'})
        self.assertEqual(response.status_code, 302,
                         "Doit rediriger pour un email inconnu.")

        # Suivre la redirection pour vérifier l'absence d'erreur Jinja
        response_followed = self.client.post(
            '/showSummary', data={'email': 'unknown@example.com'}, follow_redirects=True)
        self.assertEqual(response_followed.status_code, 200,
                         "Après redirection, le code doit être 200.")
        self.assertNotIn(b"UndefinedError", response_followed.data,
                         "Aucune erreur Jinja ne doit apparaître.")


if __name__ == '__main__':
    unittest.main()
