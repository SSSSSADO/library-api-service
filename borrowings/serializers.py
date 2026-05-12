from django.db import transaction
from django.db.models import F

from rest_framework import serializers

from books.serializers import BookDetailSerializer
from borrowings.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "book")

    def validate(self, attrs):
        book = attrs["book"]
        if book.inventory < 1:
            raise serializers.ValidationError("Book inventory is 0")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        book = validated_data["book"]
        user = self.context["request"].user
        book.inventory = F("inventory") - 1
        book.save()
        book.refresh_from_db()

        return Borrowing.objects.create(user=user, **validated_data)
