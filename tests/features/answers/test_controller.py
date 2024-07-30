# from unittest.mock import patch, MagicMock
# from fastapi.testclient import TestClient
# from qna_api.main import app
# import pytest

# client = TestClient(app)

# @pytest.fixture(scope="module")
# def test_client():
#     with TestClient(app) as client:
#         yield client

# @pytest.fixture
# def mock_get_password_hash():
#     with patch("qna_api.features.auth.services.get_password_hash", autospec=True) as mock_service:
#         yield mock_service

# @pytest.fixture
# def mock_create_user():
#     with patch("qna_api.features.auth.services.create_user", autospec=True) as mock_service:
#         yield mock_service

# @pytest.fixture
# def mock_db():
#     with patch("qna_api.core.database.get_db", autospec=True) as mock_db:
#         yield mock_db

# def test_create_user(test_client: TestClient, mock_get_password_hash: MagicMock, mock_create_user: MagicMock):
#     # Configurar el mock para devolver una contraseña hasheada
#     mock_get_password_hash.return_value = "hashedpassword123"

#     # Configurar el mock para simular la creación de un usuario
#     mock_user = MagicMock(id=1, username="newuser", email="newuser@example.com", full_name="New User", disabled=False)
#     mock_create_user.return_value = mock_user

#     # Ejecutar la solicitud de prueba
#     response = test_client.post("/auth/users/", json={"username": "newuser", "email": "newuser@example.com", "full_name": "New User", "password": "password123"})

#     # Validar la respuesta
#     assert response.status_code == 200
#     data = response.json()
#     assert data["username"] == "newuser"
#     assert data["email"] == "newuser@example.com"
#     assert "id" in data

# def test_authenticate(test_client: TestClient, mock_db: MagicMock):
#     mock_session = mock_db.return_value.__enter__.return_value
#     mock_user = MagicMock(username="testuser", hashed_password="hashedpassword123")
#     mock_session.query.return_value.filter.return_value.first.return_value = mock_user

#     with patch("qna_api.features.auth.services.verify_password", return_value=True):
#         with patch("qna_api.features.auth.services.create_access_token", return_value="testtoken"):
#             response = test_client.post("/auth/token", data={"username": "testuser", "password": "password123"})
#             assert response.status_code == 200
#             data = response.json()
#             assert data["access_token"] == "testtoken"
#             assert data["token_type"] == "bearer"

# def test_login_with_invalid_credentials(test_client: TestClient, mock_db: MagicMock):
#     mock_session = mock_db.return_value.__enter__.return_value
#     mock_session.query.return_value.filter.return_value.first.return_value = None

#     response = test_client.post("/auth/token", data={"username": "testuser", "password": "wrongpassword"})
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Incorrect username or password"}
