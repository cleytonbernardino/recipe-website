from django.test import RequestFactory
from django.urls import reverse

from recipes.models import Recipe
from utils.pagination import make_pagination, make_pagination_rage

from .test_recipe_base import RecipeTestBase


class PaginationTest(RecipeTestBase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,

        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)

        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=15,
        )['pagination']
        self.assertEqual([14, 15, 16, 17], pagination)

    def test_make_pagination_range_is_static_when_lest_page_next(self):
        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_rage(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=23,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_if_the_page_is_float_the_page_must_be_1(self):
        factory = RequestFactory()
        response = factory.get(reverse('recipes:home'))
        for n in range(5):
            self.make_recipe(
                slug=str(n),
                author_data={'username': str(n)}
            )
        recipes = Recipe.objects.all()
        page_obj, page_range = make_pagination(
            response,
            recipes,
            per_page=9,
        )['pagination']
        ...
