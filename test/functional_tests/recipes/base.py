from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def make_login(self):
        string_pass = 'testPassword'
        user = User.objects.create_user(
            username='testUser', password=string_pass
        )

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Type you username"]')
        password_field = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Type you password"]')

        username_field.send_keys(user.username)
        password_field.send_keys(string_pass)
        form.submit()
