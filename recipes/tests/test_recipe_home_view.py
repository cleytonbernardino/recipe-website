from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

    def test_view_home(self):
        view = resolve('/')  # ou reverse("recipes:home")
        self.assertIs(view.func, views.home)

    def test_view_home_status_code_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_view_home_loads_corret_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_templates_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            "<h2 style='text-align: center; padding: 4rem;'>No Recipes Have Been Published Yet 😅</h2>",  # noqa: E501
            response.content.decode('utf-8'),
        )

    def test_recipe_home_templates_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('UTF-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_templates_dont_load_recipes_not_published(self):
        """Test if is_published is False show Recipe"""

        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('UTF-8')
        response_context_recipes = response.context['recipes']

        self.assertEqual(len(response_context_recipes), 0)
        self.assertIn(  # This test does the same as the one above, it's just for learning even this one  # noqa: E501
           "<h2 style='text-align: center; padding: 4rem;'>No Recipes Have Been Published Yet 😅</h2>",  # noqa: E501
          content)  # noqa: E131
