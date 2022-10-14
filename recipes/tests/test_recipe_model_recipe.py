from django.core.exceptions import ValidationError
from parameterized import parameterized
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):

    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(
                name='Category test for is_html_false'),
            author=self.make_author(
                username='Author test for is_html_false'),
            title='Recipe Title',
            description='Uma Descrição',
            slug='Recipe-no-Default',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porção',
            preparation_steps='Recipe Preparation Steps',
            cover='media/recipes/covers/2022/09/06/Captura_de_Tela_1_A\
                ovTgzu.png'
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_maz_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_prepartion_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='the preparation_steps_is_html is not True')

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published,
                         msg='the is_published is not True')

    def test_recipe_string_representation(self):
        needed = 'Test Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(needed), 'Test Representation',
            msg=f'Recipe String representation must be "{needed}" but\
                "{str(self.recipe)}"'
        )
