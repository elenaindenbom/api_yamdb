from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    """Категория произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug категории'
    )

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Жанр произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug жанра'
    )

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Произведение."""
    name = models.CharField(
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',  # год выпуска не может быть больше текущего
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,  # требуется указать уже существующие категорию и жанр
        verbose_name='Жанр',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,  # не нужно удалять связанные с этим жанром произведения
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,  # не нужно удалять связанные с этой категорией произведения
    )

    @property
    def rating(self):
        return self.reviews.all().aggregate(rating=models.Avg('score')).get('rating')

    def year_validation(self, value):
        if value > datetime.now().year:
            raise ValidationError('Год выпуска не может быть в будущем!')

    def __str__(self) -> str:
        return self.name
