import datetime as dt

from django.shortcuts import get_object_or_404
from titles.models import Title, Category, Genre
from rest_framework import filters, viewsets, mixins, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    ReviewsSerializer,
    CommentsSerializer,
    SignUpSerializer,
)
from .permissions import IsAdminOrReadOnly
from users.models import User
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response


class SignUpAPIView(APIView):
    """
    Анонимный пользователь высылает JSON c "email" и "username".
    В ответ на почту получает confirmation_code.
    Создается новый пользователь.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            send_mail(
                "Subject here",
                "string Код подтвержения",
                "from@example.com",
                [serializer.data.get("email")],
                fail_silently=False,
            )
            User.objects.create(**serializer.validated_data, role="user")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    """
    Пользователь с правами admin высылает JSON c "email" и "username".
    Создается новый пользователь.
    """

    # TODO permission_classes = (IsAdminUser,)
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create(**serializer.validated_data, role="user")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
