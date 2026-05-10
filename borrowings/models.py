from django.conf import settings
from django.db import models

from rest_framework.exceptions import ValidationError

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    def clean(self):
        if self.expected_return_date < self.borrow_date:
            raise ValidationError(
                "Expected return date must be after borrow date"
            )
        if  self.actual_return_date < self.borrow_date:
            raise ValidationError(
                "Actual return date can't be earlier than borrow date"
            )
