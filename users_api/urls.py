from django.urls import path  # , include

# from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ClientUserCreateView,
    UserManagementView,
    EmailTokenObtainPairView,
    UserCollectionView,
)  # Add this import

# from .views import UserViewSet

# TODO: Disable this urls in production, they allow creating users without any authentication
# router = DefaultRouter()
# router.register(r"users", UserViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path("token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),  # Use custom view
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("self_register/", ClientUserCreateView.as_view(), name="client_user_create"),  # POST to create client user
    path("users/", UserCollectionView.as_view(), name="user_management"),
    path(
        "users/<int:user_id>/", UserManagementView.as_view(), name="user_management"
    ),  # PUT and DELETE for user management
]
