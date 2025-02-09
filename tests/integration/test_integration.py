# tests/integration/test_integration.py

import unittest
import os
import json
from app.server import app


class TestServerRoutes(unittest.TestCase):
    """
    Test d'intégration pour vérifier qu'une réservation de 3 places
    aboutit à un message de succès ('Great-booking complete!').
    """

    def setUp(self):
        """
        Prépare l'application Flask en mode TEST et un client de test.
        Si nécessaire, réinitialisez ici vos fichiers JSON
        (par ex. copy test_clubs.json et test_competitions.json).
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Exemple (optionnel) : si vous avez un paramètre pour surcharger
        # l'emplacement des fichiers clubs/competitions en mode test,
        # vous pouvez le faire ici (non détaillé).

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
            "/purchasePlaces",
            data=data,
            follow_redirects=True
        )

        # Vérifie qu'on obtient un code 200
        self.assertEqual(
            response.status_code,
            200,
            "La requête /purchasePlaces doit retourner un code 200 (OK)."
        )

        # Vérifie qu'on obtient bien le message de succès
        # (ex. "Great-booking complete!")
        lowercase_data = response.data.lower()
        self.assertIn(
            b"great-booking complete!",
            lowercase_data,
            "Doit contenir un message de réservation réussie ('Great-booking complete!')."
        )

        # Vous pouvez ajouter d'autres checks ici, par ex. vérifier que
        # le nombre de places du club et/ou le nombre de points restants
        # s'affichent correctement dans la page renvoyée.


if __name__ == "__main__":
    unittest.main()
