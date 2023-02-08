from os import environ

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForm, RegisterForm
from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(environ.get('PER_PAGE', 6))


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(request, 'You user is created, please log in.')
        del (request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


def login_create(request):
    POST = request.POST
    if not POST:
        messages.error(request, 'invalid credentials')
        raise Http404()

    form = LoginForm(POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, 'You are logged in.')
            return redirect('authors:dashboard')

    messages.error(request, 'invalid credentials')
    return redirect('authors:login')


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
        messages.error(request, 'invalid logout request')
        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect('authors:login')

    logout(request)
    messages.success(request, 'logged out successfully')
    return redirect('authors:login')
