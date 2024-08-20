from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.views.generic import FormView

from authors.forms import AuthorRecipeForm
from recipes.models import Recipe


class DashboardRecipe(FormView, LoginRequiredMixin):
    login_url = 'authors:login'
    template_name = 'authors/pages/dashboard-recipe.html'
    form_class = AuthorRecipeForm
    success_url = 'authors:dashboard_recipe_edit'

    def get_recipe(self, id: int, raise_except: bool = True):
        try:
            return Recipe.objects.get(
                pk=id,
                is_published=False,
                author=self.request.user
            )
        except Recipe.DoesNotExist:
            if raise_except:
                raise Http404()
            return None

    def form_valid(self, form):
        form.clean()
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        if recipe.slug == "":
            recipe.slug = slugify(recipe.title)
        recipe.save()
        messages.success(self.request, _('Your recipe has been successfully saved!'))
        return redirect(reverse(self.success_url, kwargs={
            "pk": recipe.pk
        }))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        pk = self.kwargs.get('pk', None)
        if pk is None:
            return form_kwargs

        form_kwargs.update({
            'data': self.request.POST or None,
            'instance': self.get_recipe(pk),
            'files': self.request.FILES or None,
        })
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.get_recipe(
            self.kwargs.get('pk', 0), raise_except=False
        )
        return context


class DashboardRecipeDelete(DashboardRecipe):

    def post(self, request):
        pk = request.POST.get('pk', 0)
        recipe = self.get_recipe(pk)
        recipe.delete()
        messages.success(request, _('Delete successfully.'))
        return redirect('authors:dashboard')
