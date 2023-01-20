from django.contrib.auth.models import User
from django.urls import reverse
from pytest import mark
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):

    def get_form(self):
        return self.browser.find_element(By.CLASS_NAME, 'main-form')

    def test_user_valid_data_can_login_successfully(self):
        string_pass = 'testPassword'
        user = User.objects.create_user(
            username='testUser', password=string_pass
        )

        # Úsuario abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Úsuario vê o formulario de login
        form = self.get_form()
        username_field = self.get_by_placeholder(form, 'Type you username')
        password_field = self.get_by_placeholder(form, 'Type you password')

        # Úsuario digita seu úsuario e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_pass)
        # Úsuario envia o formulario
        form.submit()

        # Úsuario vê a mensagem de login com sucesso
        self.assertIn(
            'You are logged in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # Úsuario abre a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Úsuario vê os campos usuario e senha
        form = self.get_form()
        username_field = self.get_by_placeholder(form, 'Type you username')
        password_field = self.get_by_placeholder(form, 'Type you password')

        # Úsuario digita úsuario e senha incorreto
        username_field.send_keys('username')
        password_field.send_keys('password')

        # Úsuario envia o formulario
        form.submit()

        # Úsuario vísualiza uma mensage de erro
        self.assertIn(
            'invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
