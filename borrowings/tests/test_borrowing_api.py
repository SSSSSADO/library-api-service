from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from borrowings.models import Borrowing


BORROWING_URL = reverse("borrowings:borrowings-list")

def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_book(**params):
    defaults = {
        "title": "Test Book",
        "author": "Test Author",
        "inventory": 5,
        "daily_fee": 10,
        "cover": "SOFT",
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class BorrowingApiTests(APITestCase):
    def setUp(self):
        self.user = create_user(
            email="user@test.com",
            password="test12345",
            first_name="Danil",
            last_name="Test"
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing(self):
        book = create_book()
        payload = {
            "borrow_date": str(date.today()),
            "expected_return_date": str(
                date.today() + timedelta(days=7)
            ),
            "book": book.id,
        }
        response = self.client.post(BORROWING_URL, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        borrowing = Borrowing.objects.get(id=response.data["id"])
        self.assertEqual(
            borrowing.user,
            self.user
        )
        book.refresh_from_db()
        self.assertEqual(book.inventory, 4)

    def test_create_borrowing_inventory_zero(self):
        book = create_book(inventory=0)
        payload = {
            "borrow_date": date.today(),
            "expected_return_date": date.today() + timedelta(days=7),
            "book": book.id,
        }
        response = self.client.post(BORROWING_URL, payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_borrowings_list_only_for_current_user(self):
        another_user = create_user(
            email="test@gmail.com",
            password="test_password",
        )
        book = create_book()
        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            book=book,
            user=self.user,
        )
        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            book=book,
            user=another_user,
        )
        response = self.client.get(BORROWING_URL)
        self.assertEqual(len(response.data), 1)

    def test_return_borrowing(self):
        book = create_book(inventory=2)
        borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            book=book,
            user=self.user,
        )
        url = reverse(
            "borrowings:borrowings-return-borrowing",
            args=[borrowing.id]
        )
        response = self.client.post(url)
        borrowing.refresh_from_db()
        book.refresh_from_db()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertIsNotNone(
            borrowing.actual_return_date
        )
        self.assertEqual(book.inventory, 3)
