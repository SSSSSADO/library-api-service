from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ForeignKey(
        "Book", on_delete=models.CASCADE, related_name="borrowed_books"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="borrowed_users"
    )
