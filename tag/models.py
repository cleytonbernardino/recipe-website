from random import SystemRandom
from string import ascii_letters, digits

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    # Campos de relação generica
    # Representa os models que queremos encaixar
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Representa o id da linha do model descrito acima
    object_id = models.CharField(max_length=40)
    # Um campo que represeta a relação genérica que conhece os
    # Campos acima (content_type e objects_id)
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    ascii_letters + digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name