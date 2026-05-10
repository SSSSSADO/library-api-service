from datetime import date

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingDetailSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related("book", "user")
        user = self.request.user
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        if is_active == "true":
            queryset = queryset.filter(actual_return_date__isnull=False)
        if is_active == "false":
            queryset = queryset.filter(actual_return_date__isnull=True)

        if user.is_staff:
            if user_id:
                queryset = queryset.filter(user_id=user_id)
            return queryset

        return queryset.filter(user=user)

    @action(detail=True, methods=["post"], url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            return Response(
                {"detail": "Borrowing already returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = date.today()
        book = borrowing.book
        book.inventory += 1
        book.save()
        borrowing.save()
        serializer = self.get_serializer(borrowing)

        return Response(serializer.data, status=status.HTTP_200_OK)
