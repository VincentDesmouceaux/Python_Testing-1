"""
Test du module `server` pour la page welcome (cas d'email inconnu).

Contient plusieurs tests visant à vérifier que la route `/showSummary`
réagit correctement face à un email inconnu, ou à un appel en GET non autorisé.
"""

import unittest
from app.server import app


class TestWelcomePage(unittest.TestCase):
    """
    Classe de tests pour la page de résumé (welcome.html),
    en particulier lorsque l'email transmis n'existe pas en base.
    """

    def setUp(self):
        """
        Configure l'application Flask en mode TEST.
        Crée un client de test pour simuler des requêtes HTTP.
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_show_summary_unknown_email_redirects(self):
        """
        Vérifie qu'un email inconnu provoque une redirection (302).
        Puis s'assure qu'il n'y a pas d'erreur Jinja dans la page finale.
        """
        response = self.client.post(
            '/showSummary', data={'email': 'unknown@example.com'}
        )
        self.assertEqual(
            response.status_code,
            302,
            "La route doit rediriger pour un email inconnu."
        )

        # On suit la redirection pour vérifier le code final
        response_followed = self.client.post(
            '/showSummary', data={'email': 'unknown@example.com'}, follow_redirects=True
        )
        self.assertEqual(
            response_followed.status_code,
            200,
            "Après la redirection, on s'attend à un code 200."
        )
        self.assertNotIn(
            b"UndefinedError",
            response_followed.data,
            "Aucune erreur Jinja ne doit être présente."
        )

    def test_show_summary_no_undefined_error_for_unknown_email(self):
        """
        Scénario similaire (email_inconnu@example.com) : vérifie encore
        l'absence d'erreur Jinja et la redirection 302, puis code 200.
        """
        response = self.client.post(
            '/showSummary', data={'email': 'email_inconnu@example.com'}
        )
        self.assertEqual(
            response.status_code,
            302,
            "Redirection attendue pour un email inconnu."
        )
        response_followed = self.client.post(
            '/showSummary',
            data={'email': 'email_inconnu@example.com'},
            follow_redirects=True
        )
        self.assertEqual(response_followed.status_code, 200)
        self.assertNotIn(b'UndefinedError', response_followed.data)

    def test_show_summary_get_method_not_allowed(self):
        """
        Vérifie que la route /showSummary (prévue en POST) ne répond pas en GET,
        ou répond par une redirection. Souvent, Flask renvoie 405 Method Not Allowed.
        """
        response = self.client.get('/showSummary')
        # Selon la config, Flask peut renvoyer 405, 302 ou 308.
        self.assertIn(
            response.status_code,
            [302, 405],
            "GET /showSummary n'est pas autorisé (on attend 405 ou redirection)."
        )


if __name__ == '__main__':
    unittest.main()
