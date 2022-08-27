from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для POST, PATCH, DEL."""

    def validate_year(self, value):
        if value > datetime.now().year:
            raise ValidationError('Год выпуска не может быть в будущем!')

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        slug_field='slug'
    )
    year = serializers.IntegerField(
        validators=[validate_year]
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для GET."""

    rating = serializers.IntegerField()
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
