from rest_framework import viewsets
from reviews.models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserGetTokenSerializer
)
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код подтверждения регистрации',
                f'{confirmation_code}',
                'yamdb.host@yandex.ru',
                [serializer.validated_data.get('email')],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGetTokenView(APIView):
    def post(self, request):
        serializer = UserGetTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            token = request.data.get('confirmation_code')
            confirmation_code = default_token_generator.check_token(
                user, token)
            if not confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
