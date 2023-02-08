from django.test import TestCase
from django.urls import reverse


class RecipeURLSTest(TestCase):
    def test_url_recipe_home(self):
        self.assertEqual(reverse('recipes:home'), '/')

    def test_url_recipe_category(self):
        self.assertEqual(reverse('recipes:category',
                                 kwargs={'category_id': 1}), '/recipes/category/1/')

    def test_url_recipe_recipe(self):
        url = reverse('recipes:recipe', kwargs={'pk': 2})
        self.assertEqual(url, '/recipes/2/')

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
