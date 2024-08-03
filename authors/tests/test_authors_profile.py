from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from recipes.tests.test_recipe_base import RecipeMixin


class AuthorProfileTest(TestCase, RecipeMixin):

    def setUp(self, *args, **kwargs):
        self.author = self.create_author()
        return super().setUp(*args, **kwargs)

    def create_author(
        self,
        username='TestUser',
        email='emailtest@gmail.com',
        password='123'
    ):

        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

    # Achar um nome melhor
    def test_is_returning_a_404_if_there_are_no_authors(self):
        response = self.client.get(reverse('authors:profile_detail', kwargs={
            'id': self.author.pk + 1
        }))
        self.assertEqual(response.status_code, 404)

    def test_is_only_loading_published_recipes(self):
        self.make_recipe(
            author_data=self.author,
            title='Recipe is not published',
            slug='Recipe-Test-slug',
            is_published=False
        )
        self.make_recipe(author_data=self.author, title='Recipe is published')

        response = self.client.get(reverse('authors:profile_detail', kwargs={
            'id': self.author.pk
        }))

        self.assertNotIn('Recipe is not published', response.content.decode())
        self.assertIn('Recipe is published', response.content.decode())

    def test_is_only_loading_user_recipes(self):
        self.make_recipe(author_data=self.author, title='First Recipe')
        self.make_recipe(title='Test Recipe', slug='Test-Recipe')

        response = self.client.get(reverse('authors:profile_detail', kwargs={
            'id': self.author.pk
        }))
        self.assertIn('First Recipe', response.content.decode())
        self.assertNotIn('Test Recipe', response.content.decode())
