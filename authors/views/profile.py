from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views import View
from os import environ

from authors.models import Profile
from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(environ.get('PER_PAGE', 6))

class ProfileView(View):
    template_name = 'authors/pages/profile.html'

    def get(self, request, id: int):
        profile = get_object_or_404(
                Profile.objects.filter(pk=id).select_related('author'),
                pk=id
            )
        author = User.objects.get(pk=id)
        recipes = Recipe.objects.filter(author=author, is_published=True)\
            .select_related('category').prefetch_related('author').order_by('-id')
        
        page_obj, page_range = make_pagination(request, recipes, PER_PAGE)

        return render(request, self.template_name, {
            'profile': profile,
            'recipes': page_obj,
            'pagination_range': page_range,
        })
