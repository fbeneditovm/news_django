import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users_api.models import User
from utils.global_values import USER_PROFILES, ARTICLE_COLUMNS


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        email="admin@test.com",
        password="admin_password",
        name="Admin User",
        user_profile=USER_PROFILES[0][0],  # EMP
        is_admin=True,
        employee_id="EMP001",
    )


@pytest.fixture
def employee_user():
    return User.objects.create_user(
        email="employee@test.com",
        password="employee_password",
        name="Employee User",
        user_profile=USER_PROFILES[0][0],  # EMP
        is_admin=False,
        employee_id="EMP002",
    )


@pytest.fixture
def client_user():
    return User.objects.create_user(
        email="client@test.com",
        password="client_password",
        name="Client User",
        user_profile=USER_PROFILES[1][0],  # CLI
        plan="INFO",
        accessible_columns=[ARTICLE_COLUMNS[0][0]],  # POW
    )


@pytest.mark.django_db
class TestUserAPI:
    def test_create_client_user(self, api_client):
        url = reverse("client_user_create")
        data = {
            "email": "newclient@test.com",
            "password": "client_password",
            "name": "New Client",
            "user_profile": USER_PROFILES[1][0],  # CLI
            "plan": "INFO",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newclient@test.com").exists()

    def test_token_obtain(self, api_client, admin_user):
        url = reverse("token_obtain_pair")
        data = {"email": "admin@test.com", "password": "admin_password"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_admin_can_create_employee(self, api_client, admin_user):
        # Login as admin
        token = self._get_token(api_client, admin_user.email, "admin_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("user_management")
        data = {
            "email": "newemployee@test.com",
            "password": "emp_password",
            "name": "New Employee",
            "user_profile": USER_PROFILES[0][0],
            "employee_id": "EMP003",
            "is_admin": False,
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_client_cannot_create_employee(self, api_client, client_user):
        token = self._get_token(api_client, client_user.email, "client_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("user_management")
        data = {
            "email": "newemployee@test.com",
            "password": "emp_password",
            "name": "New Employee",
            "user_profile": USER_PROFILES[0][0],
            "employee_id": "EMP003",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def _get_token(self, api_client, email, password):
        url = reverse("token_obtain_pair")
        response = api_client.post(url, {"email": email, "password": password}, format="json")
        return response.data["access"]
