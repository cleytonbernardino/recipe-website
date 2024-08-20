from django.urls import reverse
from django.utils.translation import gettext as _
from parameterized import parameterized
from pytest import mark
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):

    def __init__(self, *args, **kwargs):
        self.form_data = {
            'title': 'Title for recipe',
            'description': 'Form recipe description',
            'preparation_time': 10,
            'preparation_time_unit': 'Horas',
            'servings': '3',
            'servings_unit': 'Pessoas',
            'preparation_steps': 'Preparation steps for recipe the test \
                text for complete the 50 chars',
        }
        super().__init__(*args, **kwargs)

    def fill_form_dummy_data(self, form, value=' ' * 20):

        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(value)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

    @parameterized.expand([
        ('Type your First Name here', 'Write your first name'),  # first_name
        ('You Last Name', 'Write your last name'),  # last_name
        ('You Username', 'This field must be not empty'),  # username
        ('Type your Password here', 'This field must be not empty'),  # password # noqa: E501
        ('Confirm the Password', 'Please repeat you password'),  # password2
    ])
    def test_empty_fields_error(self, placeholder, error_menssage):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.get_form()

        self.fill_form_dummy_data(form, value='Afs213!$ds')
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        field = self.get_by_placeholder(form, placeholder)
        field.clear()
        field.send_keys(' ' * 20)
        field.send_keys(Keys.ENTER)

        form = self.get_form()

        self.assertIn(error_menssage, form.text)

    def test_invalid_email_erro_menssage(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.get_form()

        self.fill_form_dummy_data(form)

        email = self.get_by_placeholder(form, 'Ex: email@example.com')
        email.clear()
        email.send_keys('invalid@email')
        email.send_keys(Keys.ENTER)

        form = self.get_form()

        self.assertIn('The E-mail must be valid.', form.text)

    def test_password_do_not_match(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()

        password = self.get_by_placeholder(form, 'Type your Password here')
        password2 = self.get_by_placeholder(form, 'Confirm the Password')

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        password.send_keys('P4ssw0rd#')
        password2.send_keys('P4ssw0rd#_Different')
        password2.send_keys(Keys.ENTER)

        form = self.get_form()
        self.assertIn(
            'Confirm the password, it must be the same as the password',
            form.text)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()

        self.get_by_placeholder(
            form, 'Type your First Name here').send_keys('Alipio')
        self.get_by_placeholder(form, 'You Last Name').send_keys('dos Santos')
        self.get_by_placeholder(form, 'You Username').send_keys('AlipioSantos')
        self.get_by_placeholder(
            form, 'Ex: email@example.com').send_keys('AlipioSantos@email.com')
        self.get_by_placeholder(
            form, 'Type your Password here').send_keys('P4ssw0rd!Strong')
        self.get_by_placeholder(
            form, 'Confirm the Password').send_keys('P4ssw0rd!Strong')

        form.submit()

        self.assertIn(
            _('You user is created, please log in.'),
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    @parameterized.expand([
        ('title', 8, 'Title must at least 8 chars'),
        ('description', 20, 'Description must at least 20 chars'),
        ('preparation_steps', 60, 'Preparation steps must at least 60 chars'),
    ])
    def test_min_length_title_field(self, field, min_length, error_msg):
        self.make_login()
        # Usuário abre na pagina de nova receita
        self.browser.get(
            self.live_server_url + reverse('authors:dashboard_recipe'))

        # Usuário vê o formulario e preenche ele de forma incorreta
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[3]/form[2]')
        self.form_data[field] = 's' * (min_length - 1)

        for fi, value in self.form_data.items():
            input_field = form.find_element(By.NAME, fi)
            input_field.send_keys(value)

        # Usuário envia o formulário
        form.submit()

        # Usuário confirma o envio do formulário
        self.browser.find_element(By.ID, 'confirm-button-yes').click()

        # Usuário vê o erro em sua tela
        self.assertIn(error_msg,
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_title_is_the_same_as_description(self):
        self.make_login()

        self.browser.get(
            self.live_server_url + reverse('authors:dashboard_recipe'))

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[3]/form[2]')

        self.form_data['title'] = 'title is the same as description'
        self.form_data['description'] = 'title is the same as description'

        for field, value in self.form_data.items():
            input_field = form.find_element(By.NAME, field)
            input_field.send_keys(value)
        form.submit()

        # Usuário confirma o envio do formulário
        self.browser.find_element(By.ID, 'confirm-button-yes').click()

        self.assertIn('Cannot be equal to',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_preparation_time_and_servings_only_accepts_positive_values(self):
        self.make_login()

        # Usuário entra na pagina de cadastro de receitas
        self.browser.get(
            self.live_server_url + reverse('authors:dashboard_recipe'))

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[3]/form[2]')

        self.form_data['preparation_time'] = '-1'
        self.form_data['servings'] = '-3y'

        for field, value in self.form_data.items():
            input_field = form.find_element(By.NAME, field)
            input_field.send_keys(value)
        form.submit()

        # Usuário confirma o envio do formulário
        self.browser.find_element(By.ID, 'confirm-button-yes').click()

        self.assertIn('cannot be less than 0',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_send_recipes_successfully(self):
        self.make_login()
        self.browser.get(
            self.live_server_url + reverse('authors:dashboard_recipe'))

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div/div[3]/form[2]')

        for field, value in self.form_data.items():
            input_field = form.find_element(By.NAME, field)
            input_field.send_keys(value)
        form.submit()

        # Usuário confirma o envio do formulário
        self.browser.find_element(By.ID, 'confirm-button-yes').click()

        self.assertIn(_("Your recipe has been successfully saved!"),
                      self.browser.find_element(By.TAG_NAME, 'body').text)
