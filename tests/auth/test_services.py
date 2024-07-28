from qna_api.auth.service import get_password_hash, verify_password, authenticate_user, create_access_token
from qna_api.domain.user import UserEntity
from datetime import timedelta

def test_get_password_hash():
    password = "password123"
    hashed_password = get_password_hash(password)
    assert hashed_password != password

def test_verify_password():
    password = "password123"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)

def test_authenticate_user(mock_db_session):
    mock_user = UserEntity(username="testuser", email="testuser@example.com", full_name="Test User", hashed_password=get_password_hash("password123"))
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    authenticated_user = authenticate_user(mock_db_session, "testuser", "password123")
    assert authenticated_user
    assert authenticated_user.username == "testuser"

def test_create_access_token():
    data = {"sub": "testuser"}
    expires = timedelta(minutes=15)
    token = create_access_token(data, expires)
    assert token
