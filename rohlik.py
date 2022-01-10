import datetime
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

BASE_URL = "https://www.rohlik.cz"
SCREENSHOTS_URL = os.environ.get("SCREENSHOTS_URL", "screenshots")


class Rohlik:
    def __init__(self, email, password, headless):
        self._email = email
        self._password = password
        self._last_login = None

        options = Options()
        options.headless = headless
        self._driver = webdriver.Firefox("/usr/local/bin/", options=options)
        self._driver.set_window_size(1440, 1440)

        self._sleep_interval = (0.1, 0.2)

    def login(self):
        self._navigate(f"{BASE_URL}/uzivatel/profil")
        self._sleep()

        if "prihlaseni" not in self._driver.current_url:
            # already logged in
            return

        self._click_on_button("Allow all")  # hide cookies
        self._fill_input("email", self._email)
        self._fill_input("password", self._password)
        self._click_on_button("Přihlásit se")
        self._last_login = datetime.datetime.now()
        self._sleep()

    def ensure_logged_in(self):
        if self._has_recently_logged_in():
            return
        self.login()

    def add_item(self, slug, amount=1):
        self.ensure_logged_in()
        self._navigate(f"{BASE_URL}/{slug}")
        self.save_screenshot()

        failures = 0
        while amount > 0 and failures <= 1:
            clicked = self._click_on_button("Přidat jeden kus.", "aria-label")
            if clicked:
                amount -= 1
            else:
                failures += 1

        if amount > 0:
            print(f"Failed to insert requested amount of {slug}, {amount} missing.")

    def save_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        norm_url = self._driver.current_url.rsplit("/", 1)[-1]
        file_name = f"{SCREENSHOTS_URL}/{timestamp}-{norm_url}.png"

        num_retries = 5
        while not self._driver.save_screenshot(file_name):
            num_retries -= 1
            print(f"Failed to save screenshot; will retry {num_retries} times")
            self._sleep()
            if num_retries <= 0:
                break

    def close(self):
        self._driver.close()

    def _navigate(self, url, reload=False):
        if not reload and self._driver.current_url == url:
            return
        self._driver.get(url)
        self._sleep()

    def _has_recently_logged_in(self, max_delay=datetime.timedelta(minutes=30)):
        if self._last_login is None:
            return False
        return self._last_login + max_delay >= datetime.datetime.now()

    def _fill_input(self, input_id, value):
        element = self._driver.find_element(By.ID, input_id)
        element.send_keys(value)
        self._sleep()

    def _click_on_button(self, value, attribute="innerText"):
        buttons = self._driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if button.get_attribute(attribute) == value:
                button.click()
                self._sleep()
                return True
        return False

    def _sleep(self):
        time.sleep(random.uniform(*self._sleep_interval))
