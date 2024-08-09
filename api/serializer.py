from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_steps', 'updated_at', 'cover', 'category',
            'author', 'public', 'tags'
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)

    def validate_title(self, title):
        try:
            Recipe.objects.get(title=title)
        except Recipe.DoesNotExist:
            return title
        raise serializers.ValidationError("This title is already in use")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email'
        ]
