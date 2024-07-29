import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta, timezone
from qna_api.auth.service import get_admin_user, get_authenticated_user
from qna_api.main import app  
from qna_api.core.config import settings
from qna_api.user.repository import UserRepository
from qna_api.domain.user import UserEntity

# Configure Test Client
client = TestClient(app)

# Create Fake UserRepository so that this test doesn't depend on the actual database
class FakeUserRepository(UserRepository):
    _instance = None
    def __init__(self):
        self.users = {
            "testuser": UserEntity(
                username="testuser",
                roles="user",
                hashed_password="$2b$12$KIX/Qd/bZ5at5fYniGkZkeWGyVgt9DZyZye69psA3kFhi5LbYEmBu"  # 'password' hashed
            ),
            "admin": UserEntity(
                username="admin",
                roles="user,admin",
                hashed_password="$2b$12$KIX/Qd/bZ5at5fYniGkZkeWGyVgt9DZyZye69psA3kFhi5LbYEmBu" # 'password' hashed
            )
        }
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    
    def get_by_username(self, username: str) -> UserEntity | None:
        return self.users.get(username)

@pytest.fixture
def authenticated_user_token():
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"sub": "testuser", "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


@pytest.fixture
def authenticated_admin_token():
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"sub": "admin", "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def test_get_authenticated_user(authenticated_user_token):
    app.dependency_overrides[UserRepository.instance] = FakeUserRepository.instance

    response = client.get("/some_protected_route", headers={"Authorization": f"Bearer {authenticated_user_token}"})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser"}

def test_unauthenticated_user():    
    app.dependency_overrides[UserRepository.instance] = FakeUserRepository.instance

    response = client.get("/some_protected_route")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_authenticated_admin(authenticated_admin_token):
    app.dependency_overrides[UserRepository.instance] = FakeUserRepository.instance

    response = client.get("/some_admin_only_route", headers={"Authorization": f"Bearer {authenticated_admin_token}"})
    assert response.status_code == 200
    assert response.json() == {"username": "admin"}

def test_unauthenticated_admin():    
    app.dependency_overrides[UserRepository.instance] = FakeUserRepository.instance

    response = client.get("/some_admin_only_route")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_unauthorized_admin(authenticated_user_token):    
    app.dependency_overrides[UserRepository.instance] = FakeUserRepository.instance

    response = client.get("/some_admin_only_route", headers={"Authorization": f"Bearer {authenticated_user_token}"})
    assert response.status_code == 403
    assert response.json() == {"detail": "You do not have the necessary permissions"}  

# Sample route for testing that requires authenticated users
@app.get("/some_protected_route")
def some_protected_route(current_user: UserEntity = Depends(get_authenticated_user)):
    return {"username": current_user.username}

# Sample route for testing only reacheable by admin users
@app.get("/some_admin_only_route")
def some_protected_route(current_user: UserEntity = Depends(get_admin_user)):
    return {"username": current_user.username}
