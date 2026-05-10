from django.urls import path, include
from rest_framework import routers
from users.views import UserViewSet


app_name = "users"

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [path("", include(router.urls)),]