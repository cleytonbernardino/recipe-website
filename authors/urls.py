from django.urls import path

from . import views

app_name = 'authors'


urlpatterns = [
    path('register/', views.AuthorRegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashbord, name='dashboard'),
    path(
        'dashboard/recipe/',
        views.DashboardRecipe.as_view(), name="dashboard_recipe"
    ),
    path(
        'dashboard/recipe/<int:pk>/',
        views.DashboardRecipe.as_view(), name="dashboard_recipe_edit"
    ),
    path(
        'dashboard/recipe/delete/',
        views.DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete'
    ),
    path(
        'profile/<int:id>/',
        views.ProfileView.as_view(), name='profile_detail'
    ),
    path(
        'profile/updateProfile/',
        views.ProfileView.as_view(), name='profile_update_profile'
    ),
    path('profile/search/', views.author_search, name='profile_search'),
]
