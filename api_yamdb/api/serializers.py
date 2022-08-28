from datetime import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ('title',)
        # read_only_fields = ('author', )
        model = Review

    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        user = self.context['request'].user
        title = get_object_or_404(Title, id=title_id)
        if (title.reviews.filter(author=user).exists()
           and self.context.get('request').method == 'POST'):
            raise serializers.ValidationError(
                'К каждому произведению можно оставить только один отзыв!'
            )
        return data

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                'Оценка должна быть целым числом от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ('review',)
        # read_only_fields = ('author', 'post',)
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя не может быть me!')
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя не может быть me!')
        return value


class UserGetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для POST, PATCH, DEL."""

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )

    def validate_year(self, value):
        if value > datetime.now().year:
            raise ValidationError('Год выпуска не может быть в будущем!')


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для GET."""

    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

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
