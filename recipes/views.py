from os import environ

from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView, ListView

from tag.models import Tag
from utils.pagination import make_pagination

from .models import Recipe

PER_PAGE = int(environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, page_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update({
            'recipes': page_obj,
            'pagination_range': page_range,
            'search_term': '',
            'additional_url_query': ''})

        return ctx


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True,
        )
        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({'title': f'{ctx["recipes"][0].category.name} - Category'})
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'
    search_term = None

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        self.search_term = self.request.GET.get('search', '').strip()
        if not self.search_term:
            raise Http404()

        qs = qs.filter(
            Q(
                Q(description__icontains=self.search_term) |
                Q(title__icontains=self.search_term)
            ),
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'search_term': self.search_term,
            'page_title': f'search for "{self.search_term}"',
            'additional_url_query': f'&search={self.search_term}'
        })
        return ctx


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', ''))

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
            'page_title': f'search for "{page_title}"',
        })
        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/detail-recipe.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True,
            'search_term': '',
            'additional_url_query': '',
        })
        return ctx
