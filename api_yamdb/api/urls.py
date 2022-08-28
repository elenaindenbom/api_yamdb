from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserGetTokenView,
                    UserRegistrationView, UserViewSet)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='comment'
)
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
v1_router.register('users', UserViewSet, basename='user')

v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('v1/auth/token/', UserGetTokenView.as_view(), name='token'),
]
