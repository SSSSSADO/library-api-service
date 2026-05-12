from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from users.models import User


BOOKS_URL = reverse("books:book-list")


def detail_url(book_id):
    return reverse("books:book-detail", args=[book_id])


def sample_book(**params):
    defaults = {
        "title": "Test Book",
        "author": "Test Author",
        "cover": Book.Cover.SOFT,
        "inventory": 5,
        "daily_fee": "10.00",
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class PublicBookApiTests(APITestCase):
    def test_list_books(self):
        sample_book()
        sample_book(title="Second Book")

        response = self.client.get(BOOKS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book_detail(self):
        book = sample_book()

        url = detail_url(book.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], book.id)
        self.assertEqual(response.data["title"], book.title)
        self.assertIn("inventory", response.data)


class PrivateBookApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="test12345",
            is_staff=True,
        )
        self.client.force_authenticate(self.admin)

    def test_create_book(self):
        payload = {
            "title": "New Book",
            "author": "New Author",
            "cover": Book.Cover.HARD,
            "inventory": 3,
            "daily_fee": "15.50",
        }

        response = self.client.post(BOOKS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(id=response.data["id"])
        self.assertEqual(book.title, payload["title"])

    def test_update_book(self):
        book = sample_book()

        url = detail_url(book.id)
        payload = {"inventory": 10}

        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book.refresh_from_db()
        self.assertEqual(book.inventory, 10)
