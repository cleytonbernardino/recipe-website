from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from recipes.tests.test_recipe_base import RecipeMixin


class AuthorsDashboard(TestCase, RecipeMixin):

    def logout(self):
        self.client.logout()

    def setUp(self) -> None:
        User.objects.create_user(
            username='my_username', password='my_password')
        self.client.login(username='my_username', password='my_password')
        return super().setUp()

    def test_return_404_if_not_found_recipe(self):
        response = self.client.get(
            reverse('authors:dashboard_recipe_edit', kwargs={'id': 1}))

        self.assertEqual(404, response.status_code)

    def test_dashboard_recipe_delete_return_404_if_method_not_POST(self):
        response = self.client.get(reverse('authors:dashboard_recipe_delete'))

        self.assertEqual(404, response.status_code)

    def test_dashboard_recipe_delete_return_404_if_is_published_true(self):
        recipe = self.make_recipe(is_published=True, author_data={'id': 1})
        self.client.login(username=recipe.author.username,
                          password='my_password')

        response = self.client.post(reverse('authors:dashboard_recipe_delete'), data={
            'id': 1,
        })

        self.assertEqual(404, response.status_code)

    def test_dashboard_recipe_delete_return_404_if_author_not_correct(self):
        self.make_recipe(is_published=False)
        response = self.client.post(
            reverse('authors:dashboard_recipe_delete'), data={
                'id': 1,
            })

        self.assertEqual(404, response.status_code)

    def test_dashboard_recipe_delete_success(self):
        recipe = self.make_recipe(is_published=False, author_data={'id': 1})
        recipe2 = self.make_recipe(
            title='recipe_delete', slug='recipe-delete', is_published=False,
            author_data={'id': 1})
        response = self.client.post(reverse('authors:dashboard_recipe_delete'), data={
            'id': recipe2.pk
        }, follow=True)

        decode = response.content.decode('UTF-8')

        self.assertIn(recipe.title, decode)
        self.assertIn('Delete successfully.', decode)
