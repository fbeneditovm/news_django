from rest_framework import viewsets, permissions
from drf_yasg.utils import swagger_auto_schema
from .models import NewsArticle
from .serializers import NewsArticleSerializer
from django.db import models
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model

User = get_user_model()


class IsEmployeeOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow employees to create/edit/delete articles.
    Clients can only read published articles they have access to.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True

        return request.user.is_employee

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        if not request.user.is_employee:
            return False

        if request.user.is_admin:
            return True

        return obj.author == request.user


class NewsArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing news articles.

    list:
    Return a list of all news articles the user has access to.

    create:
    Create a new news article (employee only).

    retrieve:
    Return the given news article if user has access.

    update:
    Update the given news article (employee only, admin can update any).

    partial_update:
    Partially update the given news article (employee only, admin can update any).

    destroy:
    Delete the given news article (employee only, admin can delete any).
    """

    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployeeOrReadOnly]

    @swagger_auto_schema(
        operation_description="List news articles based on user's access level",
        responses={200: NewsArticleSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new news article (employee only)",
        request_body=NewsArticleSerializer,
        responses={201: NewsArticleSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return NewsArticle.objects.none()

        if user.is_admin:
            return NewsArticle.objects.all()

        if user.is_employee:
            return NewsArticle.objects.filter(models.Q(status="PUBD") | models.Q(author=user))

        return NewsArticle.objects.filter(status="PUBD").filter(
            models.Q(column__in=user.accessible_columns) | models.Q(column="")  # Empty column means accessible to all
        )

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_employee:
            serializer.save(author=self.request.user)
        else:
            raise NotFound("Not Found")
