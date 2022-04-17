from email.policy import default

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Comments, Reviews
from titles.models import Category, Genre, Title
from users.models import User


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
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Reviews
        exclude = ("title",)
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(), fields=("title", "author")
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

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
    role = serializers.CharField(default="user")

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
