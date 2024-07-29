from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    profile_picture = models.ImageField(
        upload_to='authors/pictures/%Y/%m/%d/', null=True, blank=True
    )

    def __str__(self):
        return self.author.username

    def get_absolute_url(self) -> str:
        return reverse('authors:profile_detail', args=(self.pk,))

    def save(self, *args, **kwargs):
        if self.bio == '':
            self.bio = f'Hello my name is {self.author.username}'

        return super().save(*args, **kwargs)
