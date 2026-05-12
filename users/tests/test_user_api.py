from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


USER_URL = reverse("users:users-list")
TOKEN_URL = reverse("token_obtain_pair")
ME_URL = reverse("users:users-me")

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(APITestCase):
    def test_create_user(self):
        payload = {
            "email": "test@gmail.com",
            "password": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        response = self.client.post(USER_URL, payload)
        user = get_user_model().objects.get(
            email=payload["email"]
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertTrue(
            user.check_password(payload["password"])
        )
        self.assertNotIn("password", response.data)

    def test_create_token(self):
        user_details = {
            "email": "test@gmail.com",
            "password": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class PrivateUserApiTests(APITestCase):
    def setUp(self):
        self.user = create_user(
            email="user@example.com",
            password="testpass123",
            first_name="Danil",
            last_name="Test",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_profile(self):
        response = self.client.get(ME_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["email"],
            self.user.email
        )

    def test_update_profile(self):
        payload = {
            "first_name": "NewName"
        }

        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            self.user.first_name,
            payload["first_name"]
        )
