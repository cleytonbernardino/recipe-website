from os import environ

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView

from authors.forms import LoginForm, RegisterForm
from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(environ.get('PER_PAGE', 6))


class AuthorRegisterView(FormView):
    template_name = 'authors/pages/register_view.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(
            self.request,
            _('You user is created, please log in.')
        )
        return redirect(reverse('authors:login'))


class LoginView(FormView):
    template_name = 'authors/pages/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        if not form.login(self.request):
            messages.error(
                self.request,
                _('invalid credentials')
            )
            return redirect(reverse('authors:login'))
        messages.success(
            self.request,
            _('You are logged in.')
        )
        return redirect(reverse('authors:dashboard'))


def author_search(request):
    author_username = request.GET.get('search', '')
    authors = User.objects.filter(username__startswith=author_username[1:])

    return render(request, 'authors/pages/search.html', context={
        'authors': authors,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashbord(request):
    recipes = Recipe.objects.filter(
        author=request.user, is_published=False
    ).order_by('-pk')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'authors/pages/dashbord.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, _('invalid logout request'))
        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        messages.error(request, _('Invalid logout user'))
        return redirect('authors:login')

    logout(request)
    messages.success(request, _('logged out successfully'))
    return redirect('authors:login')
