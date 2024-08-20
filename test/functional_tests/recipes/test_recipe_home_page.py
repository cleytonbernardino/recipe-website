from unittest.mock import patch

from django.utils.translation import gettext as _
from pytest import mark
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from recipes.tests.test_recipe_base import RecipeMixin

from .base import RecipeBaseFunctionalTest


@mark.functional_test
class RecipeHomePageFunctionTest(RecipeBaseFunctionalTest, RecipeMixin):

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(f'{_("No Recipes Have Been Published Yet")} 😅', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_fing_correct_recipe(self):
        recipes = self.make_recipe_in_batch()

        # Usuario abre o navegador
        self.browser.get(self.live_server_url)

        # Usuario visualiza um campo de busca com o texto "Search for a recipe..." # noqa: E501
        search_placeholder = _('Search for a recipe or @author')
        search_input = self.browser.find_element(
            By.XPATH,
            f'//input[@placeholder="{search_placeholder}"]'
        )

        # Clica no input e digita "Recipe title"
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        # O úsuario vê o que estáva procurando na pagina
        self.assertIn(
            recipes[0].title,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuario abre a página
        self.browser.get(self.live_server_url)

        # Vê que tem uma páginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )

        page2.click()

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
