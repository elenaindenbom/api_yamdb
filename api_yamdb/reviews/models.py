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


class Review(models.Model):
    text = models.CharField('Текст отзыва', max_length=200)
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    title = models.ForeignKey(
        Titles,
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
