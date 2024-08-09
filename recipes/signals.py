"""
    Django signal handling module
"""

from os import path, remove

from django.conf import settings
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from recipes.models import Recipe


def delete_cover(instance):
    """
        Delete the cover of the received instance.\n
        If the instance does not have a cover, nothing happens.
    """
    try:
        placeholder_path = path.join(settings.BASE_DIR, 'media\\missionImage.jpg')
        if instance.cover.path == placeholder_path:
            return
        remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        pass


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    """
        Removes the previous cover from the files if it has been changed or
        removed.
    """
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return

    if old_instance.cover != instance.cover:
        delete_cover(old_instance)


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    """
        After a recipe is deleted, this sign deletes the cover to save space.
    """
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if old_instance:
        delete_cover(old_instance)
