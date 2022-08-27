from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = [
        (MODERATOR, 'Модератор'),
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

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Category(models.Model):
    """Категория произведения."""

    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        'Slug категории',
        max_length=50,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Жанр произведения."""

    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        'Slug жанра',
        max_length=50,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Произведение."""

    name = models.CharField(
        'Название произведения',
    )
    year = models.IntegerField(
        'Год выпуска',
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        'Жанр',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        'Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )

    @property
    def rating(self):
        """Формирует усреднённую оценку пользователей."""

        return (self.reviews.all().aggregate(
            rating=models.Avg('score')).get('rating'))

    def __str__(self) -> str:
        return self.name
