from django.test import TestCase
from django.urls import reverse

from recipes.tests.test_recipe_base import RecipeMixin


class AuthorProfileTest(TestCase, RecipeMixin):

    def setUp(self, *args, **kwargs):
        author_raw_data = {
            'username': 'test_user',
            'password': '123',
        }
        self.logged_author = self.make_author(**author_raw_data)
        self.client.login(**author_raw_data)
        return super().setUp(*args, **kwargs)

    def get_response_detail(self, pk):
        url = reverse('authors:profile_detail', kwargs={'id': pk})
        return self.client.get(url)

    def post_respose_update(self):
        url = reverse('authors:profile_update_profile')
        return self.client.post(url)

    def test_is_returning_a_404_if_there_are_no_authors(self):
        response = self.get_response_detail(
            self.logged_author.pk + 1
        )
        self.assertEqual(response.status_code, 404)

    def test_is_only_loading_user_recipes(self):
        recipe = self.make_recipe(
            title='Not_published_recipe',
            is_published=False,
        )
        recipe.author = self.logged_author
        recipe.save()

        response = self.get_response_detail(recipe.author.pk)
        self.assertNotIn('Not_published_recipe', response.content.decode())

    def test_the_bio_can_be_changed_by_the_author(self):
        url = reverse('authors:profile_update_profile')
        response = self.client.post(url, data={
            'text-bio': 'This_is_new_bio'
        }, follow=True)
        self.assertIn(
            'This_is_new_bio',
            response.content.decode('utf-8')
        )
