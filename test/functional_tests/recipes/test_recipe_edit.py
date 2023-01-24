from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


class RecipeEdit(RecipeBaseFunctionalTest):
    def test_save_new_recipe_in_dashboard(self):
        self.make_login()
        # Úsuario abre o site na pagina de cria receita
        self.browser.get(
            self.live_server_url + reverse('authors:dashboard_recipe_new'))

        # Úsuario preenche as informação da receita e envia
        fields = {
            'title': 'Um título curto para teste',
            'description': 'Descrição da recita teste',
            'preparation_time': 1,
            'preparation_time_unit': 'Horas',
            'servings': 3,
            'servings_unit': 'Pessoas',
            'preparation_steps': 'Passo a passo da preparação da receita de teste',
            'cover': "C:\\Users\\cleytonbj\\Pictures\\Screenshots\\Captura.png",
        }
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[2]/form')

        for field, text in fields.items():
            element = form.find_element(By.NAME, field)
            element.send_keys(text)

        form.submit()
        self.assertIn("Your recipe has been successfully saved!",
                      self.browser.find_element(By.TAG_NAME, 'body').text)
