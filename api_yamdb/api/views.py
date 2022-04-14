import datetime as dt

from django.shortcuts import get_object_or_404
from titles.models import Title, Category, Genre
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer)
from .permissions import IsAdminOrReadOnly

