from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title

from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          GetTitleSerializer, TitleSerializer)


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.DestroyModelMixin):
    pass 


class CategoryViewSet(viewsets.ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('=name',)


class GenreViewSet(viewsets.ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleSerializer или GetTitleSerializer
    # https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset
    permission_classes = [AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('name', 'year', 'genre', 'category')

    def get_serializer_class(self):
        if self.request.method is 'GET':
            return GetTitleSerializer
        return TitleSerializer
