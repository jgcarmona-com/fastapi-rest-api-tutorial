from fastapi.testclient import TestClient
from qna_api.main import app
import pytest

client = TestClient(app)

def test_create_question(client: TestClient, mock_db_session):
    response = client.post("/questions/", json={"title": "Sample Question", "description": "This is a sample question"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Sample Question"
    assert data["description"] == "This is a sample question"

def test_get_questions(client: TestClient, mock_db_session):
    response = client.get("/questions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_question_by_id(client: TestClient, mock_db_session):
    response = client.get("/questions/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_get_nonexistent_question(client: TestClient, mock_db_session):
    response = client.get("/questions/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}
