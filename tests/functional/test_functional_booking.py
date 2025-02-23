# tests/functional/test_functional_booking.py

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestFunctionalBooking(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:5000"

    def tearDown(self):
        self.driver.quit()

    def test_book_places_selenium(self):
        driver = self.driver
        driver.get(self.base_url)

        # 1) Saisir l'email -> Se connecter
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("admin@irontemple.com")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 2) welcome.html => "Réserver" (Spring Festival)
        link = driver.find_element(By.LINK_TEXT, "Réserver")
        link.click()

        # 3) booking.html => Saisir 3 places
        places_input = driver.find_element(By.ID, "places")
        places_input.send_keys("3")
        # Désormais on clique spécifiquement le bouton id="submit-booking"
        driver.find_element(By.ID, "submit-booking").click()

        # 4) Attente explicite d'apparition du flash
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".flashes")))

        # 5) Vérification
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        self.assertIn("great-booking complete!", body_text)


if __name__ == "__main__":
    unittest.main()
