from django.test import TestCase
from django.urls import reverse


class RecipeURLSTest(TestCase):
    def test_url_recipe_home(self):
        self.assertEquals(reverse('recipes:home'), '/')

    def test_url_recipe_category(self):
        self.assertEquals(reverse('recipes:category',
                          kwargs={'category_id': 1}), '/recipes/category/1/')

    def test_url_recipe_recipe(self):
        url = reverse('recipes:recipe', kwargs={'id': 2})
        self.assertEqual(url, '/recipes/2/')
