import pytest
from fastapi.testclient import TestClient
from qna_api.main import app
from qna_api.auth.services import create_access_token, get_password_hash
from qna_api.core.database import SessionLocal
from qna_api.domain.user import UserEntity
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_db_session():
    with patch("qna_api.core.database.SessionLocal", autospec=True) as mock_session:
        session = mock_session.return_value
        session.query.return_value.filter.return_value.first.return_value = None
        yield session

@pytest.fixture
def auth_client(client: TestClient, mock_db_session):
    # Crear un usuario simulado sin el campo 'password'
    user_data = {"id": 1, "username": "testuser", "email": "testuser@example.com", "full_name": "Test User"}
    mock_user = UserEntity(**user_data, hashed_password=get_password_hash("password123"))
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Crear un token de acceso simulado
    token = create_access_token(data={"sub": mock_user.username})
    
    # Añadir el token al cliente de prueba
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
