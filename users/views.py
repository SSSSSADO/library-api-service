from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)

from users.models import User
from users.serializers import UserSerializer


@extend_schema_view(
    create=extend_schema(
        description="Register new user",
        responses=UserSerializer,
    ),
    me=extend_schema(
        description="Get or update current authenticated user",
        responses=UserSerializer,
    ),
)
class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        methods=["GET"],
        responses=UserSerializer,
    )
    @extend_schema(
        methods=["PUT", "PATCH"],
        request=UserSerializer,
        responses=UserSerializer,
    )
    @action(
        methods=["GET", "PUT", "PATCH"],
        detail=False,
        url_path="me"
    )
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=request.method == "PATCH"
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
