"""
Test d'intégration pour vérifier qu'une réservation de 3 places
affiche bien le message 'Great-booking complete!'.
"""

import unittest
from app.server import app


class TestServerRoutes(unittest.TestCase):
    """
    Classe de tests d'intégration sur la route /purchasePlaces et la réservation.
    """

    def setUp(self):
        """
        Configure l'appli en mode TEST et crée un client HTTP.
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_purchase_places_route(self):
        """
        Simule un POST /purchasePlaces (3 places) pour 'Iron Temple'
        dans 'Spring Festival'. Vérifie code 200 et 'Great-booking complete!'.
        """
        data = {
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "3"
        }
        response = self.client.post(
            "/purchasePlaces", data=data, follow_redirects=True)
        self.assertEqual(
            response.status_code,
            200,
            "POST /purchasePlaces (3 places) devrait retourner 200 (OK)."
        )

        # On convertit response.data en minuscules pour simplifier la recherche
        lowercase_data = response.data.lower()
        self.assertIn(
            b"great-booking complete!",
            lowercase_data,
            "Le message de réservation réussie doit apparaître."
        )


if __name__ == "__main__":
    unittest.main()
