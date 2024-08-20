from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from authors.forms import LoginForm


class AuthorsViews(TestCase):

    def test_login_form_is_not_valid(self):
        response = self.client.post(reverse('authors:login'), data={
            'username': 'Is User',
            'password': ''
        })

        form = LoginForm(response.wsgi_request.POST)
        self.assertFalse(form.is_valid())

    def test_user_tries_to_logout_using_get_methor(self):
        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')

        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertIn(
            _('invalid logout request'),
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')

        response = self.client.post(
            reverse('authors:logout'), data={
                'username': 'invalid_user',
            }, follow=True
        )

        self.assertIn(_('Invalid logout user'), response.content.decode('utf-8'))

    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')

        response = self.client.post(reverse('authors:logout'), data={
            'username': 'my_user',
        }, follow=True
        )

        self.assertIn(
            _('logged out successfully'), response.content.decode('utf-8')
        )
