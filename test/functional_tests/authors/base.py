from time import sleep as sp

from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser


class AuthorsBaseTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )

    def sleep(self, seconds=3):
        sp(seconds)
