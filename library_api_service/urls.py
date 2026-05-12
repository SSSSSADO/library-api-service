from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/books/", include("books.urls", namespace="books")),
    path("api/users/", include("users.urls", namespace="users")),
    path("api/users/token/", TokenObtainPairView.as_view()),
    path("api/users/token/refresh/", TokenRefreshView.as_view()),
    path(
        "api/borrowings/", include("borrowings.urls", namespace="borrowings")
    ),
]
