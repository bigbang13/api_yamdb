from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import unittest

from users.models import User


class CommentViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testusername")
        cls.guest_client = APIClient()
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    @unittest.expectedFailure
    def test_get_users_list(self):
        """Получить список пользователей"""
        url = "/api/v1/auth/signup/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_200(self):
        """При регистрации даны валидные данные."""
        url = "/api/v1/auth/signup/"
        data = {"email": "test@mail.ru", "username": "testusername_2"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_400(self):
        """При signup получить ошибку, если запрос с невалидными данными"""
        url = "/api/v1/auth/signup/"
        data = {}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(
            response.json(),
            {
                "email": ["This field is required."],
                "username": ["This field is required."],
            },
        )
        data = {"username": "testusername_2"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(
            response.json(), {"email": ["This field is required."]}
        )
        data = {"email": "test@mail.ru"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(
            response.json(), {"username": ["This field is required."]}
        )
        data = {"email": "testmail", "username": "testusername_2"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(
            response.json(), {'email': ['Enter a valid email address.']}
        )

    def test_signup_create_user(self):
        """Получить код подтверждения на переданный email."""
        url = "/api/v1/auth/signup/"
        data = {"email": "test@mail.ru", "username": "testusername_2"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)