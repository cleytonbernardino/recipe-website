from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func.view_class, views.RecipeListViewSearch)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?search=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_no_page_title_and_escaped(self):
        response = self.client.get(
            reverse('recipes:search') + '?search=<script>'
        )
        self.assertIn(
            'search for &quot;&lt;script&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title_one = 'This is recipe one'
        title_two = 'This is recipe two'
        recipe_one = self.make_recipe(
            title=title_one,
            slug='recipe-one',
            author_data={'username': 'one'},
        )
        recipe_two = self.make_recipe(
            title=title_two,
            slug='recipe-two',
            author_data={'username': 'two'},
        )
        response_one = self.client.get(
            reverse('recipes:search') + f'?search={title_one}'
        )
        response_two = self.client.get(
            reverse('recipes:search') + f'?search={title_two}'
        )
        response_both = self.client.get(
            reverse('recipes:search') + f'?search=this')  # noqa: F541

        self.assertIn(recipe_one, response_one.context['recipes'])
        self.assertNotIn(recipe_two, response_one.context['recipes'])

        self.assertIn(recipe_two, response_two.context['recipes'])
        self.assertNotIn(recipe_one, response_two.context['recipes'])

        self.assertIn(recipe_two, response_both.context['recipes'])
        self.assertIn(recipe_one, response_both.context['recipes'])

    def test_search_not_found_raises_html404(self):
        response = self.client.get(reverse('recipes:search') + '?search=')
        self.assertEqual(404, response.status_code)
