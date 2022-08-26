from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserRegistrationView, UserGetTokenView

app_name = 'api'


router = DefaultRouter()
# router.register('reviews', UserViewSet, basename='reviews')
# router.register('groups', GroupViewSet, basename='groups')
# router.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet, basename='comments'
# )
# router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('v1/auth/token/', UserGetTokenView.as_view(), name='token'),
]
