import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    return User.objects.create_user(
        username="testuser", password="strongpass123", is_staff=True, is_superuser=True
    )


@pytest.fixture
def auth_client(api_client, create_user):
    refresh = RefreshToken.for_user(create_user)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client
