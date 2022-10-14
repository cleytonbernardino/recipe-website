from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    def test_function_view_recipe(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_view_recipe_detail_status_code_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 10000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_templates_loads_correct_recipe(self):
        needed_title = 'This is the loaded recipe detail page   '
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={
            'id': 1
        }))
        content = response.content.decode('UTF-8')

        self.assertIn(needed_title, content)

    def test_recipe_detail_templates_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe', kwargs={
            'id': recipe.id,
        }))
        response.content.decode('utf-8')

        self.assertEqual(response.status_code, 404)
