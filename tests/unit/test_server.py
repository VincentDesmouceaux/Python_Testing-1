import unittest
from app.server import app


class TestWelcomePage(unittest.TestCase):

    def setUp(self):
        """
        Prépare l'application Flask en mode TEST.
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_show_summary_no_undefined_error_for_unknown_email(self):
        """
        Vérifie que l'application redirige (302) pour un email inconnu
        et ne produit pas d'erreur Jinja une fois la redirection suivie.
        """
        response = self.client.post(
            '/showSummary', data={'email': 'email_inconnu@example.com'})

        # On s'attend à un code 302 (redirection)
        self.assertEqual(response.status_code, 302,
                         "La route doit rediriger pour un email inconnu.")

        # Optionnel : suivre la redirection pour valider le contenu final
        response_followed = self.client.post(
            '/showSummary',
            data={'email': 'email_inconnu@example.com'},
            follow_redirects=True
        )
        # Après la redirection, on devrait avoir un code 200 (page affichée)
        self.assertEqual(response_followed.status_code, 200,
                         "Après redirection, on doit avoir un code 200.")

        # Vérifie qu'on ne voit pas 'UndefinedError' dans la page
        self.assertNotIn(b'UndefinedError', response_followed.data,
                         "Aucune erreur Jinja ne doit être présente dans la page finale.")
