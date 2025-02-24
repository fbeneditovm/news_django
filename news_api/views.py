from rest_framework import viewsets, permissions
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
    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployeeOrReadOnly]

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
