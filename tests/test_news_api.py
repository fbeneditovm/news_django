import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from news_api.models import NewsArticle
from utils.global_values import USER_PROFILES, ARTICLE_COLUMNS, PLANS, ARTICLE_STATUS

User = get_user_model()  # Get the user model dynamically


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        email="admin@test.com",
        password="admin_password",
        name="Admin User",
        user_profile=USER_PROFILES[0][0],
        is_admin=True,
        employee_id="EMP001",
    )


@pytest.fixture
def employee_user():
    return User.objects.create_user(
        email="employee@test.com",
        password="employee_password",
        name="Employee User",
        user_profile=USER_PROFILES[0][0],
        employee_id="EMP002",
    )


@pytest.fixture
def client_user():
    return User.objects.create_user(
        email="client@test.com",
        password="client_password",
        name="Client User",
        user_profile=USER_PROFILES[1][0],
        plan=PLANS[1][0],
        accessible_columns=[ARTICLE_COLUMNS[0][0]],  # POW
    )


@pytest.fixture
def client_user2():
    return User.objects.create_user(
        email="client2@test.com",
        password="client_password",
        name="Client User 2",
        user_profile=USER_PROFILES[1][0],
        plan=PLANS[0][0],
        accessible_columns=[],  # NONE
    )


@pytest.fixture
def employee_user2():
    return User.objects.create_user(
        email="employee2@test.com",
        password="employee_password",
        name="Employee User 2",
        user_profile=USER_PROFILES[0][0],
        employee_id="EMP003",
    )


@pytest.fixture
def published_article(admin_user):
    return NewsArticle.objects.create(
        title="Test Article",
        subtitle="Test subtitle",
        draft_content="Test content",
        published_content="Test content",
        original_publication_at="2024-02-24T12:00:00Z",
        last_publication_update_at="2024-02-24T12:00:00Z",
        author=admin_user,
        status="PUBD",
        column="POW",
    )


@pytest.fixture
def draft_article(employee_user):
    return NewsArticle.objects.create(
        title="Draft Article",
        subtitle="Draft subtitle",
        draft_content="Draft content",
        published_content="",  # Empty for draft
        original_publication_at="2024-02-24T12:00:00Z",
        last_publication_update_at="2024-02-24T12:00:00Z",
        author=employee_user,
        status="DRAF",
        column="TAX",
    )


@pytest.mark.django_db
class TestNewsAPI:
    def test_client_can_read_accessible_published(self, api_client, client_user, published_article):
        token = self._get_token(api_client, client_user.email, "client_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("newsarticle-detail", kwargs={"pk": published_article.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_client_cannot_read_draft(self, api_client, client_user, draft_article):
        token = self._get_token(api_client, client_user.email, "client_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("newsarticle-detail", kwargs={"pk": draft_article.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_employee_can_create_article(self, api_client, employee_user):
        token = self._get_token(api_client, employee_user.email, "employee_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("newsarticle-list")
        data = {
            "title": "New Article",
            "subtitle": "Test subtitle",
            "draft_content": "Draft content",
            "published_content": "Published content",
            "original_publication_at": "2024-02-24T12:00:00Z",
            "last_publication_update_at": "2024-02-24T12:00:00Z",
            "status": "DRAF",
            "column": "POW",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["author"] == employee_user.id

    def test_employee_can_edit_own_article(self, api_client, employee_user, draft_article):
        token = self._get_token(api_client, employee_user.email, "employee_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("newsarticle-detail", kwargs={"pk": draft_article.pk})
        data = {"title": "Updated Title"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Title"

    def test_client_cannot_create_article(self, api_client, client_user):
        token = self._get_token(api_client, client_user.email, "client_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("newsarticle-list")
        data = {
            "title": "New Article",
            "subtitle": "Test subtitle",
            "draft_content": "Draft content",
            "published_content": "",
            "original_publication_at": "2024-02-24T12:00:00Z",
            "last_publication_update_at": "2024-02-24T12:00:00Z",
            "status": "DRAF",
            "column": "POW",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_client_column_access_control(self, api_client, client_user, client_user2):
        # Create an article in POW column
        article = NewsArticle.objects.create(
            title="Power Article",
            subtitle="Test subtitle",
            draft_content="Test content",
            published_content="Test content",
            original_publication_at="2024-02-24T12:00:00Z",
            last_publication_update_at="2024-02-24T12:00:00Z",
            author=None,
            status="PUBD",
            column=ARTICLE_COLUMNS[0][0],  # POW column
        )

        # Test client with POW access can read
        token = self._get_token(api_client, client_user.email, "client_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("newsarticle-detail", kwargs={"pk": article.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Test client without POW access cannot read
        token = self._get_token(api_client, client_user2.email, "client_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_employee_article_access_control(self, api_client, employee_user, employee_user2, admin_user):
        # Create an article by employee_user
        article = NewsArticle.objects.create(
            title="Employee Article",
            subtitle="Test subtitle",
            draft_content="Test content",
            published_content="Test content",
            original_publication_at="2024-02-24T12:00:00Z",
            last_publication_update_at="2024-02-24T12:00:00Z",
            author=employee_user,
            status=ARTICLE_STATUS[0][0],
            column=ARTICLE_COLUMNS[0][0],  # POW column
        )

        # Test employee2 can read the article
        token = self._get_token(api_client, employee_user2.email, "employee_password")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("newsarticle-detail", kwargs={"pk": article.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Test employee2 cannot edit the article
        data = {"title": "Updated by employee2", "status": ARTICLE_STATUS[1][0]}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Verify the original author can still edit
        token = self._get_token(api_client, employee_user.email, "employee_password")
        data["title"] = "Updated by employee"
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated by employee"

        # Verify the admin can edit the article
        token = self._get_token(api_client, admin_user.email, "admin_password")
        data["title"] = "Updated by admin"
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated by admin"
        
        # Verify the employee2 can read the article now
        # Test employee2 cannot edit the article
        data = {"title": "Updated by admin", "status": ARTICLE_STATUS[1][0]}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated by admin"

    def _get_token(self, api_client, email, password):
        url = reverse("token_obtain_pair")
        response = api_client.post(url, {"email": email, "password": password}, format="json")
        return response.data["access"]
