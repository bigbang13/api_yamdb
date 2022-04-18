from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter,
                                           DjangoFilterBackend, FilterSet,
                                           NumberFilter)
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Reviews
from titles.models import Category, Genre, Title
from users.models import User

from .mixins import CreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly, IsAuthorOrStaff, UserPermission
from .serializers import (
    CategorySerializer,
    CommentsSerializer,
    CustomTokenObtainPairSerializer,
    GenreSerializer,
    ReviewsSerializer,
    SignUpSerializer,
    TitlePostSerializer,
    TitleSerializer,
    UserSerializer,
)


class TitleFilter(FilterSet):

    category = CharFilter(lookup_expr="slug")
    genre = CharFilter(lookup_expr="slug")
    name = CharFilter(lookup_expr="icontains")
    year = NumberFilter(field_name="year")


    class Meta:
        model = Title
        fields = ("category", "genre", "name", "year")


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleSerializer
        return TitlePostSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenreViewSet(CreateListDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class SignUpAPIView(APIView):
    """
    Анонимный пользователь высылает JSON c "email" и "username".
    В ответ на почту получает confirmation_code.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        if User.objects.filter(
            email=request.data.get("email"),
            username=request.data.get("username"),
        ).exists():
            send_mail(
                "Subject here",
                "string Код подтвержения",
                "from@example.com",
                [request.data.get("email")],
                fail_silently=False,
            )
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            serializer = SignUpSerializer(data=request.data)
            if serializer.is_valid():
                User.objects.create(**serializer.validated_data, role="user")
                send_mail(
                    "Subject here",
                    "string Код подтвержения",
                    "from@example.com",
                    [serializer.data.get("email")],
                    fail_silently=False,
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    UserPermission
    permission_classes = [UserPermission]
    pagination_class = LimitOffsetPagination
    lookup_field = "username"


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaff]
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs["title_id"])

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def rating_update(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title_id=title.id)
        title.rating = Reviews.objects.filter(title=title).aggregate(Avg("score"))
        title.save(update_fields=["rating"])

    def perform_create(self, serializer):
        title = self.get_title()
#        rating = self.rating_update
        if serializer.is_valid():
            serializer.save(
                title_id = title.id,
#                rating = rating,
                author = self.request.user
            )

    def perform_update(self, serializer):
        self.rating_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaff]
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(
            Reviews,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title__id"),
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review_id=review.id)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
