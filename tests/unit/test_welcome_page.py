# tests/unit/test_welcome_page.py

import unittest
from app.server import app


class TestWelcomePage(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_show_summary_unknown_email_redirects(self):
        """
        Vérifie qu'un email inconnu redirige (302) et ne produit pas d'erreur Jinja.
        """
        response = self.client.post(
            '/showSummary', data={'email': 'unknown@example.com'})
        self.assertEqual(response.status_code, 302,
                         "Doit rediriger pour un email inconnu.")

        response_followed = self.client.post(
            '/showSummary', data={'email': 'unknown@example.com'}, follow_redirects=True)
        self.assertEqual(response_followed.status_code, 200,
                         "Après redirection, code doit être 200.")
        self.assertNotIn(b"UndefinedError", response_followed.data,
                         "Aucune erreur Jinja ne doit apparaître.")

    def test_show_summary_no_undefined_error_for_unknown_email(self):
        """
        Variante du test (même scenario), on check juste qu'on a 200 au final.
        """
        response = self.client.post(
            '/showSummary', data={'email': 'email_inconnu@example.com'})
        self.assertEqual(response.status_code, 302,
                         "Redirection pour email inconnu.")
        response_followed = self.client.post(
            '/showSummary', data={'email': 'email_inconnu@example.com'}, follow_redirects=True)
        self.assertEqual(response_followed.status_code, 200)
        self.assertNotIn(b'UndefinedError', response_followed.data)

    def test_show_summary_get_method_not_allowed(self):
        """
        Tente un GET sur /showSummary (route prévue en POST). Vérifie qu'on a un code 405 (Method Not Allowed)
        ou potentiellement 308/302 selon config.
        """
        response = self.client.get('/showSummary')
        # Souvent Flask renvoie 405 si pas de route GET, mais ça dépend de la config
        self.assertIn(response.status_code, [
                      302, 405], "GET /showSummary n'est pas autorisé, on attend 405 ou une redirection.")


if __name__ == '__main__':
    unittest.main()
