import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class TokenViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="authorized_client")
        cls.guest_client = APIClient()
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_auth_token_post(self):
        """Получение JWT-токена в обмен на username и confirmation code."""
        url = "/api/v1/auth/token/"
        User.objects.create_user(username="testusername")
        data = {"username": "testusername", "confirmation_code": "12345"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(len(response.json()), 1)

