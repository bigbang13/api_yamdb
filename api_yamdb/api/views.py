import datetime as dt

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from titles.models import Category, Genre, Title

from .mixins import CreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewsSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")

    def perform_create(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied("Создавать может только admin!")
        if serializer.is_valid():
            serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied("Изменять может только admin!")
        super(TitleViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user.role != "admin":
            raise PermissionDenied("Удалять может только admin!")
        super(TitleViewSet, self).perform_destroy(instance)


class CategoryViewSet(CreateListDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def perform_create(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied("Создать может только admin!")
        if serializer.is_valid():
            serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user.role != "admin":
            raise PermissionDenied("Удалять может только admin!")
        super(CategoryViewSet, self).perform_destroy(instance)


class GenreViewSet(CreateListDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def perform_create(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied("Создать может только admin!")
        if serializer.is_valid():
            serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user.role != "admin":
            raise PermissionDenied("Удалять может только admin!")
        super(GenreViewSet, self).perform_destroy(instance)
