from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorsDashboard(TestCase):

    def test_return_404_if_not_found_recipe(self):
        User.objects.create_user(
            username='my_username', password='my_password')
        self.client.login(username='my_username', password='my_password')

        response = self.client.get(
            reverse('authors:dashboard_recipe_edit', kwargs={'id': 1}))

        self.assertEqual(404, response.status_code)
