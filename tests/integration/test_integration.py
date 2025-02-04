import unittest
from app.server import app


class TestServerRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_purchase_places_route(self):
        data = {
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "3"
        }
        response = self.client.post("/purchasePlaces", data=data)
        # Vérifier qu'on obtient un code 200 et un message de succès
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"booking complete", response.data.lower(),
                      "Doit contenir un message de réservation réussie.")

        # On peut ajouter des checks sur le HTML renvoyé, le nombre de places, etc.


if __name__ == "__main__":
    unittest.main()
