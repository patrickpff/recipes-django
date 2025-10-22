from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    photo = models.ImageField(
        upload_to='authors/profile/%Y/%m/%d/',
        blank=True,
        default=''
    )
