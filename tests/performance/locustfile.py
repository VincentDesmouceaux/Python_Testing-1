# tests/performance/locustfile.py

from locust import HttpUser, TaskSet, between
import time


class GUDLFTTaskSet(TaskSet):
    """
    Ensemble de tâches Locust pour GUDLFT.
    On vérifie explicitement que les GET ne dépassent pas 5s et les POST 2s.
    """

    def on_start(self):
        self.login_email = "admin@irontemple.com"

    def index(self):
        # 1) GET /
        start_t = time.time()
        resp = self.client.get("/", name="01-GET_Index")
        duration = time.time() - start_t
        if duration > 5:
            resp.failure(f"/ took {duration:.2f}s > 5s")

        # 2) POST /showSummary
        start_t = time.time()
        resp2 = self.client.post(
            "/showSummary", data={"email": self.login_email}, name="02-POST_showSummary")
        duration2 = time.time() - start_t
        # ici, on considère "showSummary" comme un chargement, donc max 5s
        if duration2 > 5:
            resp2.failure(f"showSummary took {duration2:.2f}s > 5s")

    def booking_scenario(self):
        # GET /book/Spring%20Festival/Iron%20Temple
        start_t = time.time()
        resp = self.client.get(
            "/book/Spring%20Festival/Iron%20Temple", name="03-GET_Book")
        dur = time.time() - start_t
        # C'est un GET => on impose < 5s
        if dur > 5:
            resp.failure(f"GET /book took {dur:.2f}s > 5s")

        # POST /purchasePlaces => c'est la "mise à jour", on impose < 2s
        start_t = time.time()
        resp2 = self.client.post("/purchasePlaces", data={
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "2"
        }, name="04-POST_purchasePlaces")
        dur2 = time.time() - start_t
        if dur2 > 2:
            resp2.failure(f"POST /purchasePlaces took {dur2:.2f}s > 2s")

        # GET /clubsPoints => un chargement normal, impose < 5s
        start_t = time.time()
        resp3 = self.client.get("/clubsPoints", name="05-GET_clubsPoints")
        dur3 = time.time() - start_t
        if dur3 > 5:
            resp3.failure(f"GET /clubsPoints took {dur3:.2f}s > 5s")

    tasks = {
        index: 1,
        booking_scenario: 2
    }


class GUDLFTUser(HttpUser):
    tasks = [GUDLFTTaskSet]
    # Temps d'attente entre deux scénarios
    wait_time = between(1, 3)
