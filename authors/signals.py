from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    """
    Create a profile for the user, as soon as a new user is created
    """
    if created:
        profile = Profile.objects.create(author=instance)
        profile.save()
