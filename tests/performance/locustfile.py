"""
Script Locust pour tester la performance de l'application GUDLFT.

Exécute différents scénarios (index, showSummary, booking, purchasePlaces)
et vérifie explicitement que les temps de chargement sont < 5s
et les mises à jour (purchasePlaces) < 2s.
"""

from locust import HttpUser, TaskSet, between
import time


class GUDLFTTaskSet(TaskSet):
    """
    Regroupe nos tâches de test de performance.
    Utilise un dict `tasks` au lieu de décorateurs @task.

    - index() : GET / + POST /showSummary
    - booking_scenario() : GET /book + POST /purchasePlaces + GET /clubsPoints
    """

    def on_start(self):
        """
        Méthode appelée au démarrage de chaque utilisateur virtuel (HttpUser).
        """
        self.login_email = "admin@irontemple.com"

    def index(self):
        """
        1) GET /
        2) POST /showSummary (email = admin@irontemple.com)
        Vérifie que chaque requête ne dépasse pas 5s.
        """
        start_t = time.time()
        resp = self.client.get("/", name="01-GET_Index")
        duration = time.time() - start_t
        if duration > 5:
            resp.failure(f"/ took {duration:.2f}s > 5s")

        start_t = time.time()
        resp2 = self.client.post(
            "/showSummary",
            data={"email": self.login_email},
            name="02-POST_showSummary"
        )
        duration2 = time.time() - start_t
        if duration2 > 5:
            resp2.failure(f"showSummary took {duration2:.2f}s > 5s")

    def booking_scenario(self):
        """
        1) GET /book/Spring%20Festival/Iron%20Temple (max 5s)
        2) POST /purchasePlaces (max 2s)
        3) GET /clubsPoints (max 5s)
        """
        # GET /book
        start_t = time.time()
        resp = self.client.get(
            "/book/Spring%20Festival/Iron%20Temple", name="03-GET_Book")
        dur = time.time() - start_t
        if dur > 5:
            resp.failure(f"GET /book took {dur:.2f}s > 5s")

        # POST /purchasePlaces => mise à jour => max 2s
        start_t = time.time()
        resp2 = self.client.post(
            "/purchasePlaces",
            data={
                "club": "Iron Temple",
                "competition": "Spring Festival",
                "places": "2"
            },
            name="04-POST_purchasePlaces"
        )
        dur2 = time.time() - start_t
        if dur2 > 2:
            resp2.failure(f"POST /purchasePlaces took {dur2:.2f}s > 2s")

        # GET /clubsPoints => max 5s
        start_t = time.time()
        resp3 = self.client.get("/clubsPoints", name="05-GET_clubsPoints")
        dur3 = time.time() - start_t
        if dur3 > 5:
            resp3.failure(f"GET /clubsPoints took {dur3:.2f}s > 5s")

    # Dictionnaire associant les méthodes à un "poids" (fréquence d'exécution)
    tasks = {
        index: 1,
        booking_scenario: 2
    }


class GUDLFTUser(HttpUser):
    """
    Classe d'utilisateur virtuel Locust.
    Utilise GUDLFTTaskSet comme ensemble de tâches.
    Attente (wait_time) de 1 à 3 secondes entre les tâches.
    """
    tasks = [GUDLFTTaskSet]
    wait_time = between(1, 3)
