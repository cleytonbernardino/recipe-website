from time import sleep as sp

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from django.utils.translation import gettext as _
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

    def make_login(self):
        string_pass = 'testPassword'
        user = User.objects.create_user(
            username='testUser', password=string_pass
        )

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_placeholder = _("Type you username")
        password_placeholder = _("Type you password")
        username_field = self.browser.find_element(
            By.XPATH, f'//input[@placeholder="{username_placeholder}"]')
        password_field = self.browser.find_element(
            By.XPATH, f'//input[@placeholder="{password_placeholder}"]')

        username_field.send_keys(user.username)
        password_field.send_keys(string_pass)
        form.submit()

    def sleep(self, seconds=3):
        sp(seconds)
