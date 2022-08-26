from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import Avg
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
    # сериализатор для POST, PATCH, DEL 
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
            'description',
            'genre',
            'category',
        )
    
    def year_validation(self, value):
        if value > datetime.now().year:
            raise ValidationError('Год выпуска не может быть в будущем!')
        return value


class GetTitleSerializer(serializers.ModelSerializer):
    # сериализатор для GET 
    # добавляет поле rating — устреднённая оценка пользователей (как получить?)
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

