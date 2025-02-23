"""
Test fonctionnel (Selenium) pour vérifier le parcours complet d'une réservation.

Ce test ouvre un vrai navigateur (Chrome), saisit l'email, clique sur Réserver,
saisit 3 places, et vérifie l'affichage final de 'Great-booking complete!'.
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestFunctionalBooking(unittest.TestCase):
    """
    Classe de tests fonctionnels utilisant Selenium
    pour simuler un vrai utilisateur dans le navigateur.
    """

    def setUp(self):
        """
        Initialise le driver Chrome et pointe vers http://127.0.0.1:5000
        (assure-toi que Flask tourne déjà).
        """
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:5000"

    def tearDown(self):
        """
        Ferme le navigateur à la fin du test.
        """
        self.driver.quit()

    def test_book_places_selenium(self):
        """
        Parcours fonctionnel :
         1) Accéder à /
         2) Se connecter avec 'admin@irontemple.com'
         3) Cliquer "Réserver" sur Spring Festival
         4) Saisir '3' places
         5) Vérifier le flash 'Great-booking complete!'
        """
        driver = self.driver
        driver.get(self.base_url)

        # 1) Sur index.html, saisir l'email, soumettre
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("admin@irontemple.com")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 2) Sur welcome.html, cliquer sur "Réserver" (Spring Festival)
        link = driver.find_element(By.LINK_TEXT, "Réserver")
        link.click()

        # 3) Sur booking.html, saisir 3 places
        places_input = driver.find_element(By.ID, "places")
        places_input.send_keys("3")

        # Le bouton "Réserver" a un id="submit-booking"
        driver.find_element(By.ID, "submit-booking").click()

        # 4) On attend que le flash apparaisse (<ul class="flashes">)
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".flashes")))

        # 5) Vérifie que 'great-booking complete!' est dans la page
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        self.assertIn(
            "great-booking complete!",
            body_text,
            "Le message de réservation complète doit être présent."
        )


if __name__ == "__main__":
    unittest.main()
