from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from recipes.tests.test_recipe_base import RecipeMixin


class AuthorsDashboard(TestCase, RecipeMixin):

    def logout(self):
        self.client.logout()

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='my_username', password='my_password')
        self.client.login(username='my_username', password='my_password')
        return super().setUp()

    def test_return_404_if_not_found_recipe(self):
        response = self.client.get(
            reverse('authors:dashboard_recipe_edit', kwargs={'pk': 1}))

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
        recipes = self.make_recipe_in_batch(2)
        for recipe in recipes:
            recipe.author = self.user
            recipe.is_published = False
            recipe.save()

        response = self.client.post(reverse('authors:dashboard_recipe_delete'), data={
            'pk': recipes[1].pk
        }, follow=True)

        decode = response.content.decode('UTF-8')

        self.assertIn(recipes[0].title, decode)
        self.assertIn('Delete successfully.', decode)
