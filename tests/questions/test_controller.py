import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from mediatr import Mediator
from qna_api.main import create_app
from qna_api.auth.authorization import get_admin_user, get_authenticated_user
from qna_api.user.models import User

from .models import mock_question, mock_full_question, mock_questions_list, mock_answer

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
    return User(id=1, username="testuser", full_name="Test User", email="test@example.com", roles=["user"])

@pytest.fixture
def admin_user():
    return User(id=1, username="admin", full_name="Admin User", email="admin@example.com", roles=["user,admin"])

def test_create_question(client, mediator):
    mediator.send_async.return_value = mock_question

    response = client.post("/question/", json={"title": "Sample Question", "description": "This is a sample question"})
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Sample Question"
    assert data["description"] == "This is a sample question"

def test_get_all_questions(client, mediator, admin_user):
    app = create_app(mediator=mediator)

    def _get_admin_user():
        return admin_user

    app.dependency_overrides[get_admin_user] = _get_admin_user

    with TestClient(app) as client:
        mediator.send_async.return_value = mock_questions_list

        response = client.get("/question")
        
        mediator.send_async.assert_called_once()
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        
def test_get_question_by_id(client, mediator):
    mediator.send_async.return_value = mock_question

    response = client.get("/question/1")
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_get_nonexistent_question(client, mediator):
    mediator.send_async.return_value = None

    response = client.get("/question/999")
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 404
    assert response.json() == {"detail": "Question 999 not found"}

def test_get_full_question(client, mediator):
    mediator.send_async.return_value = mock_full_question

    response = client.get("/question/1/full")
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "answers" in data
    assert len(data["answers"]) == len(mock_full_question.answers) 

def test_update_question(client, mediator):
    updated_question = mock_question.model_copy()
    updated_question.title = "Updated Question"
    updated_question.description = "This is an updated question"
    mediator.send_async.return_value = updated_question

    response = client.put("/question/1", json={"title": updated_question.title, "description": updated_question.description})
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_question.title
    assert data["description"] == updated_question.description    

def test_delete_question(client, mediator):
    mediator.send_async.return_value = mock_question

    response = client.delete("/question/1")
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_add_answer(client, mediator):
    mediator.send_async.return_value = mock_answer

    response = client.post("/question/1/answer", json={"content": "This is an answer"})
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "This is an answer"
    assert data["question_id"] == 1

def test_get_answers(client, mediator):
    mediator.send_async.return_value = mock_full_question.answers

    response = client.get("/question/1/answers")
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

# Error handling tests

def test_create_question_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.post("/question/", json={"title": "Sample Question", "description": "This is a sample question"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Test error"}

def test_get_all_questions_value_error(client, mediator, admin_user):
    app = create_app(mediator=mediator)

    def _get_admin_user():
        return admin_user

    app.dependency_overrides[get_admin_user] = _get_admin_user

    with TestClient(app) as client:
        mediator.send_async.side_effect = ValueError("Test error")

        response = client.get("/question")
        
        assert response.status_code == 400
        assert response.json() == {"detail": "Test error"}

def test_get_question_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.get("/question/1")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Test error"}

def test_get_full_question_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.get("/question/1/full")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Test error"}

def test_update_question_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.put("/question/1", json={"title": "Updated Question", "description": "This is an updated question"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Test error"}

def test_delete_question_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.delete("/question/1")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Test error"}

def test_add_answer_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.post("/question/1/answer", json={"content": "This is an answer"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Test error"}

def test_get_answers_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.get("/question/1/answers")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Test error"}