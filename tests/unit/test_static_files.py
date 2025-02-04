import unittest
from app.server import app


class TestStaticFiles(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_css_loaded(self):
        # On envoie une requête GET vers l'URL du CSS
        response = self.client.get('/static/css/style.css')
        # Vérifie que le serveur renvoie bien un code 200 (OK)
        self.assertEqual(response.status_code, 200,
                         "Le CSS devrait être accessible et retourner un code 200.")
        # Vérifie que le contenu du CSS n'est pas vide
        self.assertTrue(len(response.data) > 0,
                        "Le fichier CSS ne doit pas être vide.")
        # Optionnel : vérifier qu'une règle CSS connue est présente (ici "body")
        self.assertIn(b"body", response.data,
                      "Le CSS doit contenir la règle 'body'.")


if __name__ == '__main__':
    unittest.main()
