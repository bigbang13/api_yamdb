from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from titles.models import Category, Genre, Title
from users.models import User

TEST_USER_FIELDS: dict = {
    "username": "auth",
}

TEST_ADMIN_USER_FIELDS: dict = {"username": "admin", "role": "admin"}

TEST_GENRE_FIELDS: dict = {"name": "Ужасы", "slug": "horror"}

TEST_CATEGORY_FIELDS: dict = {"name": "Фильм", "slug": "films"}


class ReviewViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(**TEST_USER_FIELDS)
        cls.admin_user = User.objects.create_user(**TEST_ADMIN_USER_FIELDS)
        cls.genre = Genre.objects.create(**TEST_GENRE_FIELDS)
        cls.category = Category.objects.create(**TEST_CATEGORY_FIELDS)
        data = {
            "name": "Кошмар на улице Вязов",
            "year": 1984,
            "genre": cls.genre.slug,
            "category": cls.category.slug,
            "description": "Классика жанра",
        }
        cls.title = Title.objects.create(**data)

    def setUp(self):
        self.authorized_client = APIClient()
        self.authorized_client.force_login(ReviewViewsTest.user)
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(ReviewViewsTest.admin_user)
