from django.db import models


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
