from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeURLSFunction(RecipeTestBase):

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

    def test_function_view_category(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_view_category_status_code_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 10000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_templates_loads_recipes(self):
        needed_title = 'Category Test'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('UTF-8')

        self.assertIn(needed_title, content)

    def test_recipe_categort_templates_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={
            'category_id': recipe.category.id,
        }))
        response.content.decode('UTF-8')

        self.assertEqual(response.status_code, 404)

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
