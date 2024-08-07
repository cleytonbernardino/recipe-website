from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeMixin:
    def make_category(self, name='Café da Manha'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='Jose',
        last_name='Antonio',
        username='joseAntonio',
        email='joseAntonio@gmail.com',
        password='123',
        id=None,
    ):
        if id:
            return User.objects.get(pk=id)

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Uma Descrição',
        slug='Recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutos',
        servings=5,
        servings_unit='Porção',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True,
        cover='missionImage.jpg'
    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author = self.make_author()
        elif isinstance(author_data, dict):
            author = self.make_author(**author_data)
        else:
            author = author_data

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=author,
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover=cover
        )

    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = {
                'slug': f'r{i}',
                'author_data': {'username': f'user{i}'},
                'title': f'title {i}',
            }
            recipes.append(self.make_recipe(**kwargs))
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):

    def setUp(self) -> None:
        return super().setUp()
