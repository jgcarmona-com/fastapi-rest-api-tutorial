# tests/auth/test_service.py
import pytest
from unittest.mock import MagicMock, patch
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException, status
from qna_api.auth.service import AuthService
from qna_api.auth.models import TokenData
from qna_api.domain.user import UserEntity
from qna_api.core.config import settings
from qna_api.user.repository import UserRepository

@pytest.fixture(scope='module')
def mock_db_session():
    # Crear una sesión de base de datos simulada
    session = MagicMock()
    yield session

@pytest.fixture
def user_repo(mock_db_session) -> UserRepository:
    repo = UserRepository.instance(mock_db_session)
    repo.get_by_username = MagicMock()
    return repo

@pytest.fixture
def auth_service(user_repo) -> AuthService:
    return AuthService(user_repo=user_repo)

def test_authenticate_user_success(auth_service, user_repo):
    user = UserEntity(username="testuser", hashed_password="hashedpassword123")
    user_repo.get_by_username.return_value = user

    with patch.object(auth_service, '_verify_password', return_value=True) as mock_verify_password:
        authenticated_user = auth_service.authenticate_user("testuser", "password123")
        assert authenticated_user == user
        mock_verify_password.assert_called_once_with("password123", "hashedpassword123")

def test_authenticate_user_failure(auth_service, user_repo):
    user_repo.get_by_username.return_value = None
    authenticated_user = auth_service.authenticate_user("testuser", "password123")
    assert authenticated_user is None

def test_create_access_token(auth_service):
    data = {"sub": "testuser", "roles": "user"}
    token = auth_service.create_access_token(data, timedelta(minutes=15))
    decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    assert decoded["sub"] == "testuser"
    assert decoded["roles"] == "user"

@patch("qna_api.core.database.get_db", return_value=MagicMock())
def test_get_current_user_success(mock_get_db, auth_service, user_repo):
    token = auth_service.create_access_token({"sub": "testuser", "roles": "user"})
    user = UserEntity(username="testuser", hashed_password="hashedpassword123")
    user_repo.get_by_username.return_value = user

    with patch.object(AuthService, 'oauth2_scheme', return_value=token):
        with patch("qna_api.user.repository.UserRepository.instance", return_value=user_repo):
            current_user = auth_service.get_current_user(token, mock_get_db)
            assert current_user == user

@patch("qna_api.core.database.get_db", return_value=MagicMock())
def test_get_current_user_failure(mock_get_db, auth_service, user_repo):
    token = auth_service.create_access_token({"sub": "testuser", "roles": "user"})
    user_repo.get_by_username.return_value = None

    with patch.object(AuthService, 'oauth2_scheme', return_value=token):
        with patch("qna_api.user.repository.UserRepository.instance", return_value=user_repo):
            with pytest.raises(HTTPException) as excinfo:
                auth_service.get_current_user(token, mock_get_db)
            assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_password_hash(auth_service):
    password = "password123"
    hashed_password = auth_service.get_password_hash(password)
    assert hashed_password != password  # Ensure the password is hashed

def test_verify_password(auth_service):
    password = "password123"
    hashed_password = auth_service.get_password_hash(password)
    assert auth_service._verify_password(password, hashed_password)
