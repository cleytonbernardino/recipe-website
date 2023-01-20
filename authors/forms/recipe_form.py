from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_new_attr
from utils.string import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._errors = defaultdict(list)

        add_new_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_new_attr(self.fields.get('category'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_steps', 'cover', 'category'
        ]

        widgets = {
            'cover': forms.FileInput(
                attrs={'class': 'span-2'}
            ),

            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )),

            'preparation_time': forms.NumberInput(
                attrs={'min': 0}
            ),

            'preparation_time_unit': forms.Select(
                choices=(
                    ('Mínutos', 'Mínutos'),
                    ('Horas', 'Horas'),
                )),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleanded_data = self.cleaned_data

        title = cleanded_data.get('title')
        description = cleanded_data.get('description')
        preparation_time = cleanded_data.get('preparation_time')
        servings_unit = cleanded_data.get('servings_unit')

        if len(title) < 8:
            self._errors['title'].append('Title must at least 8 chars')

        if len(description) < 20:
            self._errors['description'].append(
                'Description must at least 20 chars')

        if title == description:
            self._errors['description'].append('Cannot be equal to title')
            self._errors['title'].append('Cannot be equal to description')

        if is_positive_number(preparation_time):
            self._errors[
                'preparation_time'].append(
                'Time cannot be less than 0'
            )

        if is_positive_number(servings_unit):
            self._errors['servings_unit'].append('Time cannot be less than 0')

        if self._errors:
            raise ValidationError(self._errors)

        return super_clean
