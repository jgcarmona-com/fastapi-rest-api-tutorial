from unittest.mock import MagicMock
import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException, status
from qna_api.core.config import settings
from qna_api.domain.user import UserEntity
from qna_api.features.auth.auth_service import AuthService
from qna_api.features.user.repository import UserRepository

# Create Fake UserRepository so that this test doesn't depend on the actual database
class FakeUserRepository():
    _instance = None
    def __init__(self):
        self.users = {
            "testuser": UserEntity(
                id=1,
                username="testuser",
                email="test@example.com",
                full_name="Test User",
                hashed_password="$2b$12$KIX/Qd/bZ5at5fYniGkZkeWGyVgt9DZyZye69psA3kFhi5LbYEmBu",  # 'password' hashed
                roles="user"
            ),
            "admin": UserEntity(
                id=2,
                username="admin",
                email="admin@example.com",
                full_name="Admin User",
                hashed_password="$2b$12$KIX/Qd/bZ5at5fYniGkZkeWGyVgt9DZyZye69psA3kFhi5LbYEmBu",  # 'password' hashed
                roles="admin"
            )
        }
    
    def get_by_username(self, username: str) -> UserEntity | None:
        return self.users.get(username)
    
@pytest.fixture
def user_repo():
    return MagicMock(spec=FakeUserRepository)

@pytest.fixture
def auth_service(user_repo):
    return AuthService(user_repo)

def test_create_verification_token(auth_service):
    user_id = 1
    token = auth_service.create_verification_token(user_id)
    assert token is not None
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    assert payload["user_id"] == user_id
    assert "exp" in payload

def test_create_verification_token_with_custom_expiration(auth_service):
    user_id = 1
    expires_delta = timedelta(minutes=30)
    token = auth_service.create_verification_token(user_id, expires_delta)
    assert token is not None
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    assert payload["user_id"] == user_id
    assert "exp" in payload
    expire_time = datetime.fromtimestamp(payload["exp"], timezone.utc)
    assert expire_time < datetime.now(timezone.utc) + timedelta(hours=24)

def test_decode_verification_token(auth_service):
    user_id = 1
    token = auth_service.create_verification_token(user_id)
    payload = auth_service.decode_verification_token(token)
    assert payload["user_id"] == user_id

def test_decode_verification_token_expired(auth_service):
    user_id = 1
    expires_delta = timedelta(seconds=1)
    token = auth_service.create_verification_token(user_id, expires_delta)
    import time; time.sleep(2)  # Ensure the token has expired
    with pytest.raises(HTTPException) as exc_info:
        auth_service.decode_verification_token(token)
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Token has expired"

def test_decode_verification_token_invalid(auth_service):
    invalid_token = jwt.encode({"some": "data"}, "wrong_secret", algorithm=settings.algorithm)
    with pytest.raises(HTTPException) as exc_info:
        auth_service.decode_verification_token(invalid_token)
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Invalid token"
