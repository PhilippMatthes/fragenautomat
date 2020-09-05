import pathlib

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def profile_icon_upload_path(profile, filename):
    suffix = pathlib.Path(filename).suffix
    return f'profiles/{profile.user.username}/icon{suffix}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    icon = models.ImageField(
        upload_to=profile_icon_upload_path, null=True, blank=True
    )
    icon_blurhash = models.TextField(null=True, blank=True)
    real_name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Token(models.Model):
    value = models.CharField(primary_key=True, max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Token {self.value[:6]}... for user {self.user}'
