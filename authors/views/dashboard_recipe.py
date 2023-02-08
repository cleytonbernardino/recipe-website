from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views import View

from authors.forms import AuthorRecipeForm
from recipes.models import Recipe


class DashboardRecipe(LoginRequiredMixin, View):
    login_url = 'authors:login'
    redirect_field_name = 'next'

    def get_recipe(self, id=None):
        recipe = None
        if id:
            try:
                recipe = Recipe.objects.get(
                    is_published=False,
                    author=self.request.user,
                    pk=id
                )
            except Recipe.DoesNotExist:
                raise Http404()
        return recipe

    def render_recipe(self, recipe, form):
        return render(self.request, 'authors/pages/dashboard-recipe.html',
                      context={
                          'recipe': recipe,
                          'form': form,
                      })

    def get(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            instance=recipe,
        )

        return self.render_recipe(recipe, form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            self.request.POST or None,
            files=self.request.FILES or None,
            instance=recipe,
        )

        if form.is_valid():
            form.clean()
            recipe = form.save(commit=False)
            recipe.author = self.request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            if recipe.slug == "":
                recipe.slug = slugify(recipe.title)

            recipe.save()
            messages.success(
                self.request, 'Your recipe has been successfully saved!')
            return redirect(reverse('authors:dashboard_recipe_edit', kwargs={
                'id': recipe.id,
            }))

        return self.render_recipe(recipe, form)


class DashboardRecipeDelete(DashboardRecipe):
    def get(self, request):
        raise Http404()

    def post(self, request):
        try:
            recipe = Recipe.objects.get(
                author=request.user,
                is_published=False,
                pk=request.POST['id']
            )
        except Recipe.DoesNotExist:
            raise Http404()

        recipe.delete()
        messages.success(request, 'Delete successfully.')
        return redirect('authors:dashboard')
