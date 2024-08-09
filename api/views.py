from os import environ

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.permissions import IsOwner
from api.serializer import AuthorSerializer, RecipeSerializer
from recipes.models import Recipe


class RecipeApiPagination(PageNumberPagination):
    page_size = environ.get("API_PER_PAGE", 10)


class RecipeApi(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = RecipeApiPagination
    http_method_names = ['options', 'head', 'patch', 'get', 'post', 'delete']

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            return Recipe.objects.filter(
                category_id=category_id,
                is_published=True
            )

        return qs

    def get_object(self):
        pk = int(self.kwargs.get("pk", ''))
        recipe = get_object_or_404(Recipe, pk=pk)
        if not recipe.is_published and recipe.author.pk != self.request.user.pk:
            raise Http404()
        self.check_object_permissions(self.request, recipe)

        return recipe

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class AuthorView(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(
            username=self.request.user.get_username()
        )
        return qs

    @action(
        methods=['get'],
        detail=False,
    )
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data)
