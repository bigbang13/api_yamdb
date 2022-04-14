from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ("Пользователь", "user"),
    ("Администратор", "admin"),
    ("Модератор", "moderator"),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
