from mediatr import Mediator
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from qna_api.main import create_app
from qna_api.crosscutting.authorization import get_authenticated_user
from qna_api.features.user.models import User
from .models import mock_answer, mock_updated_answer

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

def test_add_answer(client, mediator):
    mediator.send_async.return_value = mock_answer

    response = client.post("/question/1/answer", json={"content": "This is an answer"})
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "This is an answer"
    assert data["question_id"] == 1

def test_get_answer(client, mediator):
    mediator.send_async.return_value = mock_answer

    response = client.get("question/1/answer/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_answer.id
    assert data["content"] == mock_answer.content
    assert data["question_id"] == mock_answer.question_id
    assert data["user_id"] == mock_answer.user_id
    mediator.send_async.assert_called_once()

def test_get_answer_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Answer with id 1 not found")

    response = client.get("question/1/answer/1")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Answer with id 1 not found"}
    mediator.send_async.assert_called_once()

def test_update_answer(client, mediator):
    mediator.send_async.return_value = mock_updated_answer

    response = client.put("question/1/answer/1", json={"content": "This is an updated answer"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_updated_answer.id
    assert data["content"] == mock_updated_answer.content
    assert data["question_id"] == mock_updated_answer.question_id
    assert data["user_id"] == mock_updated_answer.user_id
    mediator.send_async.assert_called_once()

def test_update_answer_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Answer with id 1 not found")

    response = client.put("question/1/answer/1", json={"content": "This is an updated answer"})
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Answer with id 1 not found"}
    mediator.send_async.assert_called_once()

def test_delete_answer(client, mediator):
    mediator.send_async.return_value = mock_answer

    response = client.delete("question/1/answer/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_answer.id
    assert data["content"] == mock_answer.content
    assert data["question_id"] == mock_answer.question_id
    assert data["user_id"] == mock_answer.user_id
    mediator.send_async.assert_called_once()

def test_delete_answer_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Answer with id 1 not found")

    response = client.delete("question/1/answer/1")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Answer with id 1 not found"}
    mediator.send_async.assert_called_once()

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

def test_get_answers(client, mediator):
    mediator.send_async.return_value = [mock_answer]

    response = client.get("/question/1/answers")
    
    mediator.send_async.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
