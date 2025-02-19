# tests/functional/test_functional_booking.py

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestFunctionalBooking(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:5000"

    def tearDown(self):
        self.driver.quit()

    def test_book_places_selenium(self):
        driver = self.driver
        driver.get(self.base_url)

        # Saisir l'email et cliquer
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("admin@irontemple.com")
        submit_button = driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Cliquer sur "Réserver" (Spring Festival)
        link = driver.find_element(By.LINK_TEXT, "Réserver")
        link.click()

        # Saisir 3 places
        places_input = driver.find_element(By.ID, "places")
        places_input.send_keys("3")
        book_button = driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']")
        book_button.click()

        # Attendre la redirection
        time.sleep(1)

        # Vérifier "great-booking complete!"
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        print("DEBUG body_text:\n", body_text)
        self.assertIn("great-booking complete!", body_text)


if __name__ == "__main__":
    unittest.main()
