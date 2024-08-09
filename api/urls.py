from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import AuthorView, RecipeApi

app_name = "api"

router = SimpleRouter()
router.register('recipe', RecipeApi, basename="recipe-api")
router.register('author', AuthorView, basename='authors-api')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
