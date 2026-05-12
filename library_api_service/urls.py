from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/books/",
        include("books.urls",namespace="books"),
        name="book-list"
    ),
    path(
        "api/users/",
        include("users.urls",namespace="users"),
        name="user-list"
    ),
    path(
        "api/users/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path("api/users/token/refresh/",
         TokenRefreshView.as_view(),
         name="token_refresh"
    ),
    path(
        "api/borrowings/",
        include("borrowings.urls",namespace="borrowings",),
        name="borrowings-list"
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),
]
