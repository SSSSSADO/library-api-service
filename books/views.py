from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from drf_spectacular.utils import extend_schema

from books.serializers import BookListSerializer, BookDetailSerializer
from books.models import Book


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookDetailSerializer

    def get_permissions(self):
        permission_classes = [IsAdminUser]
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @extend_schema(
        responses=BookListSerializer
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses=BookDetailSerializer
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
