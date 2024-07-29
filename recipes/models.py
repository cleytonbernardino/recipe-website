from collections import defaultdict

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from tag.models import Tag


class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categorys')
    
    name = models.CharField(max_length=65, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class Recipe(models.Model):
    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(verbose_name=_("Preparation Time"))
    preparation_time_unit = models.CharField(max_length=65, verbose_name=_('Preparation Unit'))
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(max_length=65, verbose_name=_('Servings Unit'))
    preparation_steps = models.TextField(verbose_name=_('Preparation_steps'))
    preparation_steps_is_html = models.BooleanField(default=False, verbose_name=_('Preparation steps is html'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    is_published = models.BooleanField(default=False, verbose_name=_('is published'))
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', null=True, blank=True,
        verbose_name=_('Cover')
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None, verbose_name=_('Category')
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_('Author')
    )
    tags = models.ManyToManyField(
        Tag, blank=True, default='', verbose_name='Tags'
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('recipes:recipe', args=(self.pk,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = str(slugify(self.title))
            self.slug = slug

        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'This title is already in use'
                )

        if error_messages:
            raise ValidationError(error_messages)
