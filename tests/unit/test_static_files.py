"""
Tests unitaires pour vérifier la disponibilité des fichiers statiques
et l'absence de favicon.ico.
"""

import unittest
from app.server import app


class TestStaticFiles(unittest.TestCase):
    """
    Classe de tests pour les fichiers statiques.
    Vérifie la présence du CSS et l'absence de favicon.ico.
    """

    def setUp(self):
        """
        Initialise l'application Flask en mode TEST et récupère le client de test.
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_css_loaded(self):
        """
        Vérifie que le fichier /static/css/style.css est bien accessible et contient 'body'.
        """
        response = self.client.get('/static/css/style.css')
        self.assertEqual(
            response.status_code,
            200,
            "Le CSS doit être accessible (code 200)."
        )
        self.assertTrue(
            len(response.data) > 0,
            "Le fichier CSS ne doit pas être vide."
        )
        self.assertIn(
            b"body",
            response.data,
            "Le CSS doit contenir la règle 'body'."
        )

    def test_favicon_404(self):
        """
        Vérifie que /favicon.ico renvoie 404,
        puisqu'aucun favicon n'est défini dans ce projet.
        """
        response = self.client.get('/favicon.ico')
        self.assertEqual(
            response.status_code,
            404,
            "Pour un favicon inexistant, on s'attend à un 404."
        )


if __name__ == '__main__':
    unittest.main()
