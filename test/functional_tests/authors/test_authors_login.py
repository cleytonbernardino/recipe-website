from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _
from pytest import mark
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):

    def get_form(self):
        return self.browser.find_element(By.CLASS_NAME, 'main-form')

    def test_user_valid_data_can_login_successfully(self):
        user_data = {
            "username": "testUser",
            "password": "passwordTest"
        }
        User.objects.create_user(**user_data)

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê o formulario de login
        form = self.get_form()
        username_field = self.get_by_placeholder(form, _('Type you username'))
        password_field = self.get_by_placeholder(form, _('Type you password'))

        # Usuário digita seu Usuário e senha
        username_field.send_keys(user_data['username'])
        password_field.send_keys(user_data['password'])
        # Usuário envia o formulario
        form.submit()

        # Usuário vê a mensagem de login com sucesso
        self.assertIn(
            _('You are logged in.'),
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # Usuário abre a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê os campos usuario e senha
        form = self.get_form()
        username_field = self.get_by_placeholder(form, _('Type you username'))
        password_field = self.get_by_placeholder(form, _('Type you password'))

        # Usuário digita Usuário e senha incorreto
        username_field.send_keys('username')
        password_field.send_keys('password')

        # Usuário envia o formulario
        form.submit()

        # Usuário vísualiza uma mensage de erro
        self.assertIn(
            _('invalid credentials'),
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
