from email.policy import default
<<<<<<< HEAD

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Comments, Reviews
from titles.models import Category, Genre, Title
from users.models import User
=======
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Comments, Reviews
from users.models import User, ROLE_CHOICES
from titles.models import Category, Genre, Title
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
>>>>>>> 4d48381da56ada90b83de15cabb1ba6f7a248ea1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(required=True, many=True)
    category = CategorySerializer(required=True)
    rating = serializers.SerializerMethodField(default=None)
    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
    
    def get_rating(self, obj):
        if not Reviews.objects.filter(title=obj):
            rating = None
        else:
            rating = Reviews.objects.filter(title=obj).aggregate(Avg("score"))
        return rating


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        many=False,
        queryset=Category.objects.all()
    )
    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Reviews
        exclude = ("title",)
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(), fields=("title", "author")
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comments
        exclude = ("review",)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Email должен быть уникальным."""
        lower_email = value.lower()
        if User.objects.filter(email=lower_email).exists():
            raise serializers.ValidationError("Email должен быть уникальным")
        return lower_email

    def validate_username(self, value):
        """Использовать имя 'me' в качестве username запрещено."""
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        return value

    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        default="user",
    )

    def validate_email(self, value):
        """Email должен быть уникальным."""
        lower_email = value.lower()
        if User.objects.filter(email=lower_email).exists():
            raise serializers.ValidationError("Email должен быть уникальным")
        return lower_email

    def validate_username(self, value):
        """Использовать имя 'me' в качестве username запрещено."""
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        return value

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(
        max_length=200,
        required=True,
    )
    confirmation_code = serializers.CharField(
        max_length=200,
        required=True,
    )
    password = serializers.CharField(
        # required=False,
        # read_only=True,
        default="",
        max_length=200,
    )

    def validate_username(self, value):
        """Пользователь должен существовать, иначе ошибка 404"""
        get_object_or_404(User, username=value.lower())
        return value.lower()

    def validate_confirmation_code(self, value):
        """Валидация confirmation_code"""
        lower_confirmation_code = value.lower()
        return lower_confirmation_code
