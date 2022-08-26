from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = [
        (MODER, 'Модератор'),
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    ]

    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )

    role = models.CharField(
        'Роль пользователя',
        max_length=50,
        default=USER,
        choices=USER_ROLES,
    )

    email = models.EmailField(
        'Почта',
        unique=True
    )

    def __str__(self):
        return self.username
