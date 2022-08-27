from django.shortcuts import get_object_or_404
from reviews.models import Comment, Review, Title
from rest_framework import serializers


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
