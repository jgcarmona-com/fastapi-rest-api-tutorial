# tests/features/test_controller.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from qna_api.main import create_app
from qna_api.crosscutting.authorization import get_authenticated_user
from qna_api.features.user.models import User
from qna_api.features.vote.models import VoteCreate, Vote
from mediatr import Mediator

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

def test_vote_on_question(client, mediator):
    mediator.send_async.return_value = Vote(id=1, vote_value=1, user_id=1, question_id=1, answer_id=None)

    response = client.post("/question/1/vote", json={"vote_value": 1})
    
    assert response.status_code == 200
    data = response.json()
    assert data["vote_value"] == 1
    assert data["question_id"] == 1
    mediator.send_async.assert_called_once()

def test_vote_on_question_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.post("/question/1/vote", json={"vote_value": 1})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Test error"}
    mediator.send_async.assert_called_once()

def test_vote_on_answer(client, mediator):
    mediator.send_async.return_value = Vote(id=1, vote_value=1, user_id=1, question_id=None, answer_id=1)

    response = client.post("/question/1/answer/1/vote", json={"vote_value": 1})
    
    assert response.status_code == 200
    data = response.json()
    assert data["vote_value"] == 1
    assert data["answer_id"] == 1
    mediator.send_async.assert_called_once()

def test_vote_on_answer_value_error(client, mediator):
    mediator.send_async.side_effect = ValueError("Test error")

    response = client.post("/question/1/answer/1/vote", json={"vote_value": 1})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Test error"}
    mediator.send_async.assert_called_once()
