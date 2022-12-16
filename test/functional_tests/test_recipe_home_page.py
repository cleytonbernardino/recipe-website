from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser

# From css and JS
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class RecipeHomePageFunctionTest(LiveServerTestCase):
    def test_text_recipes_not_found(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No Recipes Have Been Published Yet 😅', body)
        browser.quit()
