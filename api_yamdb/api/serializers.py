from reviews.models import Comment, Review
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ('title',)
        # read_only_fields = ('author', )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ('review',)
        # read_only_fields = ('author', 'post',)
        model = Comment
