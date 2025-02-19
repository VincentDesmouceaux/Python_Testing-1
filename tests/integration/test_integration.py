import unittest
from app.server import app


class TestServerRoutes(unittest.TestCase):
    """
    Test d'intégration pour vérifier qu'une réservation de 3 places
    aboutit à un message de succès ('Great-booking complete!').
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_purchase_places_route(self):
        """
        Envoie un POST à '/purchasePlaces' pour réserver 3 places
        pour 'Iron Temple' dans 'Spring Festival'. Vérifie qu'on obtient
        un code 200 et un message de succès ('Great-booking complete!').
        """
        data = {
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "3"
        }
        # On suit la redirection pour voir le contenu final
        response = self.client.post(
            "/purchasePlaces", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                         "La requête /purchasePlaces doit retourner un code 200 (OK).")

        lowercase_data = response.data.lower()
        self.assertIn(
            b"great-booking complete!",
            lowercase_data,
            "Doit contenir un message de réservation réussie ('Great-booking complete!')."
        )


if __name__ == "__main__":
    unittest.main()
