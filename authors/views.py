from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from recipes.models import Recipe

from .forms import AuthorRecipeForm, LoginForm, RegisterForm


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
    )
    return render(request, 'authors/pages/dashbord.html', context={
        'recipes': recipes,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    try:
        recipe = Recipe.objects.get(
            is_published=False,
            author=request.user,
            pk=id
        )
    except Recipe.DoesNotExist:
        raise Http404()

    form = AuthorRecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )

    if form.is_valid():
        form.full_clean()
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()
        messages.success(request, 'Your recipe has been successfully saved!')
        return redirect(reverse('authors:dashboard_recipe_edit', kwargs={
            'id': id,
        }))

    return render(request, 'authors/pages/dashboard-recipe.html', context={
        'recipe': recipe,
        'form': form
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_new(request):
    form = AuthorRecipeForm(
        request.POST or None,
        request.FILES or None,
    )

    if form.is_valid():
        # form.clean()
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()
        messages.success(request, 'Your recipe has been successfully saved!')
        return redirect(reverse('authors:dashboard'))

    return render(request, 'authors/pages/dashboard-recipe.html', context={
        'form': form,
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
