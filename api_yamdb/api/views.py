from django.shortcuts import get_object_or_404
from reviews.models import Comment, Review, Titles
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorOrReadOnly, ReadOnly
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

