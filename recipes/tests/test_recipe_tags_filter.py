from django.urls import reverse

from tag.models import Tag

from .test_recipe_base import RecipeTestBase


class RecipeTagsFilterTest(RecipeTestBase):

    def test_recipes_are_being_filtered_by_tags(self):
        tags = (
            Tag.objects.create(name="TagTest", slug="tag-test"),
        )
        recipe = self.make_recipe()
        recipe.tags.set(tags)
        recipe.save()

        recipe_no_tag = self.make_recipe(
            title="cannot appear",
            slug="cannot-appear",
            author_data={"username": "antonio"}
        )

        response = self.client.get(
            reverse('recipes:tag', kwargs={
                "slug": tags[0].slug
            })
        )
        decode = response.content.decode("utf-8")
        self.assertIn(
            recipe.title,
            decode
        )
        self.assertNotIn(
            recipe_no_tag.title,
            decode
        )
