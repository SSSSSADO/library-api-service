from django.contrib.auth.models import Permission

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.serializers import Serializer

from books.serializers import BookListSerializer, BookDetailSerializer
from books.models import Book


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self) -> Serializer:
        if self.action == "list":
            return BookListSerializer
        return BookDetailSerializer

    def get_permissions(self) -> list[Permission]:
        permission_classes = [IsAdminUser]
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
