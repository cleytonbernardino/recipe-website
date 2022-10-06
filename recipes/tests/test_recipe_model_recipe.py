from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):

    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_fields_maz_length(self):
        fields = [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ]

        for field, max_lenght in fields:
            setattr(self.recipe, field, 'A' * (max_lenght + 1))
            with self.assertRaises(ValidationError):
                self.recipe.full_clean()
