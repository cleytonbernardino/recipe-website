from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms.register_form import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('first_name', 'Type your First Name here'),
        ('last_name', 'You Last Name'),
        ('username', 'You Username'),
        ('email', 'Ex: email@example.com'),
        ('password', 'Type your Password here'),
        ('password2', 'Confirm the Password'),
    ])
    def test_fields_placeholder_is_correct(self, ffield, placeholder):
        form = RegisterForm()
        current_placeholder = form[ffield].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', 'Create you username'),
        ('password2', 'The password to confirm'),
        ('email', 'The E-mail must be valid.'),
        ('password', (
            'Password must have at least one Uppercase letter, '
            'one lowercase letter, and one number. The leght should be '
            'at last 8 caracters.'
        )),
    ])
    def test_fields_help_text(self, ffield, help_text):
        form = RegisterForm()
        current_help_text = form[ffield].field.help_text
        self.assertEqual(current_help_text, help_text)

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Create a new password.'),
        ('password2', 'Confirm the Password'),
    ])
    def test_fields_label(self, ffield, label):
        form = RegisterForm()
        current_label = form[ffield].field.label
        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):

    URL = reverse('authors:register_create')

    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Str0ngPassword!3',
            'password2': 'Str0ngPassword!3',

        }
        return super().setUp(*args, **kwargs)

    def make_response_post(self, data, url='', follow=True):
        if url == '':
            url = self.URL
        return self.client.post(url, data=data, follow=follow)

    @parameterized.expand([
        ('username', 'This field must be not empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'Email is required'),
        ('password', 'This field must be not empty'),
        ('password2', 'Please repeat you password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''

        response = self.make_response_post(self.form_data, self.URL)
        self.assertIn(msg, response.content.decode('UTF-8'))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'g'
        response = self.make_response_post(self.form_data, self.URL)

        msg = 'Username must have at last 4 characters'
        self.assertIn(msg, response.content.decode('UTF-8'))

    def test_username_field_max_length_should_be_50(self):
        self.form_data['username'] = 'a' * 152
        response = self.make_response_post(self.form_data, self.URL)

        msg = 'User character limit is 50'
        self.assertIn(msg, response.content.decode('UTF-8'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'avg'
        response = self.make_response_post(self.form_data, self.URL)
        msg = (
            '<li>Password must have at least one Uppercase letter, '
            'one lowercase letter, and one number. The lenght should be '
            'at last 8 characters.</li>'
        )
        self.assertIn(msg, response.content.decode('UTF-8'))

    def test_password_field_not_have_lower_upper_case_letters_and_numbers(self):  # noqa: E501
        response = self.make_response_post(self.form_data, self.URL)
        msg = (
            '<li>Password must have at least one Uppercase letter, '
            'one lowercase letter, and one number. The lenght should be '
            'at last 8 characters.</li>'
        )
        self.assertNotIn(msg, response.content.decode('UTF-8'))

    def test_password_and_password2_confirmation_are_equal(self):
        self.form_data['password'] = 'Passw0rd!'
        self.form_data['password2'] = 'Passw0rd2!'

        msg = 'Confirm the password, it must be the same as the password'

        response = self.make_response_post(self.form_data, self.URL)
        self.assertIn(msg, response.content.decode('UTF-8'))

    def test_email_field_must_be_unique(self):
        self.client.post(self.URL, data=self.form_data, follow=True)
        response = self.client.post(self.URL, data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('UTF-8'))

    def test_author_created_can_login(self):
        self.form_data.update({
            'username': 'testUser',
            'email': 'test@gmail.com',
            'password': 't3st!inG',
            'password2': 't3st!inG',
        })
        self.make_response_post(self.form_data)
        is_authenticated = self.client.login(
            username='testUser',
            password='t3st!inG',
        )

        self.assertTrue(is_authenticated)

    def test_sand_get_request_to_registration_create_view_returns_404(self):
        response = self.client.get('authors:register_create')
        self.assertEqual(404, response.status_code)
