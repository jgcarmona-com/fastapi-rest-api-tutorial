from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import pytest
from datetime import timedelta  # Add this import
from qna_api.main import app
from qna_api.auth.auth_service import AuthService
from qna_api.auth.controller import AuthController
from qna_api.core.config import settings  # Make sure to import settings

# Fixture for the test client
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

# Fixture for the authentication service
@pytest.fixture
def auth_service():
    return MagicMock(spec=AuthService)

# Fixture for the authentication controller
@pytest.fixture
def auth_controller(auth_service):
    controller = AuthController(auth_service=auth_service)
    app.include_router(controller.router, prefix="/auth")
    return controller

@patch.object(AuthService, 'authenticate_user')
@patch.object(AuthService, 'create_access_token')
def test_authenticate_success(mock_create_access_token, mock_authenticate_user, client, auth_service, auth_controller):
    # Mock the methods of the service
    mock_authenticate_user.return_value = MagicMock(username="testuser", roles=["user"])
    mock_create_access_token.return_value = "testtoken"

    # Simulate form data
    form_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Simulate the request
    response = client.post("/auth/token", data=form_data)

    # Log the response for debugging
    print("Response status code:", response.status_code)
    print("Response body:", response.json())

    # Check the result
    assert response.status_code == 200
    assert response.json() == {"access_token": "testtoken", "token_type": "bearer"}

    # Ensure that the mock methods were called as expected
    mock_authenticate_user.assert_called_once_with("testuser", "testpassword")
    mock_create_access_token.assert_called_once_with(data={"sub": "testuser", "roles": ["user"]}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))

@patch.object(AuthService, 'authenticate_user')
def test_authenticate_failure(mock_authenticate_user, client, auth_service, auth_controller):
    # Mock the authentication method to return None
    mock_authenticate_user.return_value = None

    # Simulate form data
    form_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    # Simulate the request
    response = client.post("/auth/token", data=form_data)

    # Log the response for debugging
    print("Response status code:", response.status_code)
    print("Response body:", response.json())

    # Check the result
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

    # Ensure that the mock method was called as expected
    mock_authenticate_user.assert_called_once_with("testuser", "wrongpassword")
