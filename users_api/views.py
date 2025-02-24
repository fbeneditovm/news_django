from django.shortcuts import render
from rest_framework import viewsets, status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .serializers import UserSerializer
from utils.global_values import USER_PROFILES

# Create your views here.


# -------- Basic Views using Django default views -------- #
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# -------- Views with custom logic -------- #
class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if user is admin
        if request.user.is_admin:
            return True
        # Users can only modify their own data
        return obj.id == request.user.id


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class ClientUserCreateView(generics.CreateAPIView):
    """View for unauthenticated users to create client accounts"""

    permission_classes = []  # Allow unauthenticated access

    def get_serializer_class(self):
        class ClientUserSerializer(UserSerializer):
            user_profile = serializers.CharField(read_only=True)  # Hide user_profile field

            def create(self, validated_data):
                validated_data["user_profile"] = USER_PROFILES[1][0]  # Set to "Client"
                return super().create(validated_data)

            class Meta:
                model = User
                fields = ["email", "password", "name", "user_profile", "profile_picture"]
                extra_kwargs = {
                    "password": {"write_only": True},
                }

        return ClientUserSerializer

    def perform_create(self, serializer):
        serializer.save(
            user_profile=USER_PROFILES[1][0], is_admin=False, is_staff=False, is_superuser=False  # Set to "Client"
        )


class UserCollectionView(APIView):
    """View for managing the collection of users (list all, create new)"""

    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserManagementView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            self.check_object_permissions(request, user)

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            self.check_object_permissions(request, user)

            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            self.check_object_permissions(request, user)

            # Prevent users from deleting their own account while logged in
            if request.user.id == user_id:
                return Response(
                    {"error": "Cannot delete your own account while logged in"}, status=status.HTTP_400_BAD_REQUEST
                )

            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
