from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

USER_ROLES = [
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
    (USER, 'Пользователь'),
]


class User(AbstractUser):

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    def __str__(self):
        return self.username


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


class Review(models.Model):
    text = models.CharField('Текст отзыва', max_length=200)
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.CharField('Текст комментария', max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
