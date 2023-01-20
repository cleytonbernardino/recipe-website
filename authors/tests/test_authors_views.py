from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorsViews(TestCase):
    def test_login_create_raises_404_if_not_POST_method(self):
        request = self.client.get(reverse('authors:login_create'))
        self.assertEqual(request.status_code, 404)

    def test_user_tries_to_logout_using_get_methor(self):
        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')

        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertIn(
            'invalid logout request',
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

        self.assertIn('Invalid logout user', response.content.decode('utf-8'))

    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')

        response = self.client.post(reverse('authors:logout'), data={
            'username': 'my_user',
        }, follow=True
        )

        self.assertIn(
            'logged out successfully', response.content.decode('utf-8')
        )
