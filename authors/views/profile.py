from os import environ

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from authors.models import Profile
from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(environ.get('PROFILE_PER_PAGE', 6))


class ProfileView(View):
    template_name = 'authors/pages/profile.html'

    def get(self, request, id: int):
        context = {}

        profile = get_object_or_404(
                Profile.objects.filter(pk=id).select_related('author'),
                pk=id
            )
        author = User.objects.get(pk=id)
        context['image'] = '/media/missionImage.jpg'

        if author == self.request.user:
            context['is_owner'] = True

        if profile.profile_picture != '':
            context['image'] = profile.profile_picture.url

        recipes = Recipe.objects.filter(author=author, is_published=True)\
            .select_related('category').prefetch_related('author').order_by('-id')

        page_obj, page_range = make_pagination(request, recipes, PER_PAGE)

        context.update({
            'profile': profile,
            'recipes': page_obj,
            'pagination_range': page_range,
        })

        return render(request, self.template_name, context)

    def post(self, request):
        if request.POST.get('text-bio'):
            request.user.profile.bio = request.POST['text-bio']

        if request.FILES:
            request.user.profile.profile_picture = request.FILES['profile-image-input']

        request.user.profile.save()

        return redirect(
            reverse("authors:profile_detail", kwargs={"id": request.user.id})
        )
