import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from qna_api.main import create_app
from qna_api.user.service import UserService
from qna_api.auth.authorization import get_authenticated_user
from qna_api.user.models import User

from .models import mock_user, mock_user_create, mock_user_update, mock_updated_user

# Configure Test Client
@pytest.fixture
def client(user_service, authenticated_user):
    app = create_app(user_service=user_service)

    def _get_authenticated_user():
        return authenticated_user    

    app.dependency_overrides[get_authenticated_user] = _get_authenticated_user

    with TestClient(app) as client:
        yield client

# Mock services
@pytest.fixture
def user_service():
    return MagicMock(spec=UserService)

# Mock authenticated user
@pytest.fixture
def authenticated_user():
    return User(id=1, username="testuser", full_name="Test User", email="testuser@example.com", roles=["user"])

def test_create_user(client, user_service):
    user_service.create_user.return_value = mock_user_create

    response = client.post("/user", json={"username": "newuser", "email": "newuser@example.com", "full_name": "New User", "password": "password123"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    user_service.create_user.assert_called_once()

def test_me(client, user_service):
    response = client.get("user/me")
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert data["full_name"] == "Test User"

def test_update_user(client, user_service):
    user_service.update_user.return_value = mock_updated_user

    response = client.put("user/1", json={"username": "updateduser", "email": "updateduser@example.com", "full_name": "Updated User"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == mock_updated_user.username
    assert data["email"] == mock_updated_user.email
    assert data["full_name"] == mock_updated_user.full_name
    user_service.update_user.assert_called_once()
