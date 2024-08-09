from unittest.mock import patch

from django.urls import reverse
from parameterized import parameterized

from api.test.test_api_base import ApiTestMixin


class RecipeApiTest(ApiTestMixin):
    RECIPE_RAW_DATA = {
        "title": "WG",
        "description": "Recipe Description",
        "preparation_steps": "This is a preparation steps",
        "preparation_time": "5",
        "preparation_time_unit": "minutos",
        "servings": 3,
        "servings_unit": "pessoas"
    }

    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_response_list()
        self.assertEqual(response.status_code, 200)

    @patch('api.views.RecipeApiPagination.page_size', new=7)
    def test_recipe_api_list_is_loads_correct_number_of_recipes(self):
        wanted_numbers_of_recipe = 7
        self.make_recipe_in_batch(qtd=wanted_numbers_of_recipe)

        response = self.get_response_list()
        qtd_of_loaded_recipes = len(response.data.get('results'))

        self.assertEqual(
            wanted_numbers_of_recipe, qtd_of_loaded_recipes
        )

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        self.make_recipe(
            title="is_not_published",
            slug="is-not-published",
            is_published=False,
            author_data={'username': 'author_test_1'}
        )
        self.make_recipe(is_published=True)
        response = self.get_response_list()

        self.assertEqual(len(response.data.get('results')), 1)

    def test_recipe_api_detail_do_not_show_not_published_recipe(self):
        recipe = self.make_recipe(is_published=False)
        response = self.get_response_detail(recipe.pk)
        self.assertEqual(response.status_code, 404)

    @patch('api.views.RecipeApiPagination.page_size', new=3)
    def test_pagination_is_working_correctly(self):
        self.make_recipe_in_batch(qtd=9)

        response = self.get_response_list()        
        number_of_pages = 1
        while True:
            url = response.data.get('next', None)
            if url is None:
                break
            number_of_pages += 1
            response = self.client.get(url)
        self.assertEqual(
            number_of_pages,
            3
        )

    @patch('api.views.RecipeApiPagination.page_size', new=10)
    def test_recipe_api_list_can_loads_recipes_by_category_id(self):
        # Creates categorys
        category_wanted = self.make_category(name="Wanted")
        categort_not_wanted = self.make_category(name="Not Wanted")

        # Create 10 Recipes
        recipes = self.make_recipe_in_batch(qtd=10)

        # Change all recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # Change one recipe to the NOT Wanted Category
        # As a result, this recipe should NOT show in the page
        recipes[0].category = categort_not_wanted
        recipes[0].save()

        # Action: get recipes by wanted category_id
        category_params = f'?category_id={category_wanted.pk}'
        response = self.get_response_list(parameters=category_params)

        # We should only see recipes from wanted category
        self.assertEqual(len(response.data.get('results')), 9)

    @patch('api.views.RecipeApiPagination.page_size', new=15)
    def test_only_the_number_of_objects_defined_by_pagination_is_being_shown(self):
        # Create Recipes
        self.make_recipe_in_batch(qtd=20)

        response = self.get_response_list()
        self.assertEqual(
            len(response.data.get('results')),
            15
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        url = reverse('api:recipe-api-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_recipe_api_list_loggend_user_can_create_a_recipe(self):
        data = self.RECIPE_RAW_DATA
        access_token = self.get_author_access_data().get('access')
        response = self.client.post(
            reverse('api:recipe-api-list'), data=data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        self.assertEqual(response.status_code, 201)

    @parameterized.expand([
        ('title',),
        ('description',),
        ('preparation_time',),
        ('preparation_time_unit',),
        ('servings',),
        ('servings_unit',),
        ('preparation_steps',)
    ])
    def test_recipe_is_being_created_only_after_all_required_fields_are_submitted(self, field):
        access_token = self.get_author_access_data().get('access', '')
        recipe_raw_data = {**self.RECIPE_RAW_DATA}
        recipe_raw_data[field] = ''

        response = self.client.post(
            reverse('api:recipe-api-list'),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        self.assertEqual(
            response.status_code,
            400
        )

    def test_it_is_not_possible_to_register_two_recipes_with_the_same_name(self):
        recipe_title = "Is title"

        data = self.RECIPE_RAW_DATA
        data['title'] = recipe_title

        self.make_recipe(title=recipe_title)
        access_token = self.get_author_access_data().get('access', '')

        response = self.client.post(
            reverse('api:recipe-api-list'), data=data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        self.assertEqual(response.status_code, 400)

    def test_recipe_api_list_loggend_user_can_update_a_recipe(self):
        access_data = self.get_author_access_data()
        author = access_data["author"]

        recipe = self.make_recipe(title="old_title")
        recipe.author = author
        recipe.save()

        new_title = f"Title updated by {author.username}"

        response = self.client.patch(
            reverse('api:recipe-api-detail', kwargs={
                "pk": recipe.pk
            }),
            data={
                "title": new_title
            },
            HTTP_AUTHORIZATION=f'Bearer {access_data.get('access', '')}'
        )

        self.assertEqual(
            response.data.get('title', 'title not found'),
            new_title
        )

    def test_recipe_api_list_logged_user_cant_update_a_recipe_owner_by_another_user(self):
        recipe = self.make_recipe()
        another_user = self.get_author_access_data(username='cant_update')

        response = self.client.patch(
            reverse('api:recipe-api-detail', kwargs={
                "pk": recipe.pk
            }),
            data={
                "title": 'new title'
            },
            HTTP_AUTHORIZATION=f'Bearer {another_user.get('access', '')}'
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_only_the_recipe_author_can_delete_it(self):
        recipe = self.make_recipe()
        another_user = self.get_author_access_data(username="cant_update")

        url = reverse('api:recipe-api-detail', kwargs={'pk': recipe.pk})

        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f'Bearer {another_user.get('access', '')}'
        )

        self.assertEqual(
            response.status_code,
            403
        )
