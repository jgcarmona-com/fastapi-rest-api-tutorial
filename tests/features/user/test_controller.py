from mediatr import Mediator
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from qna_api.main import create_app
from qna_api.crosscutting.authorization import get_authenticated_user
from qna_api.features.user.models import User

from .models import mock_new_user, mock_updated_user, mock_updated_user

# Configure Test Client
@pytest.fixture
def client(mediator, authenticated_user):
    app = create_app(mediator=mediator)

    def _get_authenticated_user():
        return authenticated_user    

    app.dependency_overrides[get_authenticated_user] = _get_authenticated_user

    with TestClient(app) as client:
        yield client

# Mock mediator
@pytest.fixture
def mediator():
    return MagicMock(spec=Mediator)

# Mock authenticated user
@pytest.fixture
def authenticated_user():
    return User(id=1, username="testuser", full_name="Test User", email="testuser@example.com", roles=["user"])

def test_create_user(client, mediator):
    mediator.send_async.return_value = mock_new_user

    response = client.post("/user/signup", json={"username": "newuser", "email": "newuser@example.com", "full_name": "New User", "password": "password123"})
    
    assert response.status_code == 200
    data = response.json()
    user = data["user"]
    assert user["username"] == "newuser"
    assert user["email"] == "newuser@example.com"
    assert user["full_name"] == "New User"
    mediator.send_async.assert_called_once()

def test_create_user_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.post("/user/signup", json={"username": "newuser", "email": "newuser@example.com", "full_name": "New User", "password": "password123"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Test error"}
    mediator.send_async.assert_called_once()

def test_me(client):
    response = client.get("user/me")
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert data["full_name"] == "Test User"

def test_update_user(client, mediator):
    mediator.send_async.return_value = mock_updated_user

    response = client.put("user/1", json={"username": "updateduser", "email": "updateduser@example.com", "full_name": "Updated User"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == mock_updated_user.username
    assert data["email"] == mock_updated_user.email
    assert data["full_name"] == mock_updated_user.full_name
    mediator.send_async.assert_called_once()

def test_update_user_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.put("user/1", json={"username": "updateduser", "email": "updateduser@example.com", "full_name": "Updated User"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Test error"}
    mediator.send_async.assert_called_once()
