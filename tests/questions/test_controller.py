import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from qna_api.answers.models import AnswerCreate
from qna_api.main import create_app
from qna_api.questions.service import QuestionService
from qna_api.auth.authorization import get_admin_user, get_authenticated_user
from qna_api.user.models import User
from qna_api.questions.models import QuestionCreate

from .models import mock_question, mock_full_question, mock_questions_list, mock_answer

# Configure Test Client
@pytest.fixture
def client(question_service, authenticated_user):
    app = create_app(question_service=question_service)

    def _get_authenticated_user():
        return authenticated_user    

    app.dependency_overrides[get_authenticated_user] = _get_authenticated_user

    with TestClient(app) as client:
        yield client

# Mock services
@pytest.fixture
def question_service():
    return MagicMock(spec=QuestionService)

# Mock authenticated user
@pytest.fixture
def authenticated_user():
    return User(id=1, username="testuser", full_name="Test User", email="test@example.com", roles=["user"])

@pytest.fixture
def admin_user():
    return User(id=1, username="admin", full_name="Admin User", email="admin@example.com", roles=["user,admin"])

def test_create_question(client, question_service):
    question_service.create_question.return_value = mock_question

    response = client.post("/question/", json={"title": "Sample Question", "description": "This is a sample question"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Sample Question"
    assert data["description"] == "This is a sample question"
    question_service.create_question.assert_called_once()

def test_get_all_questions(client, question_service, admin_user):
    app = create_app(question_service=question_service)

    def _get_admin_user():
        return admin_user

    app.dependency_overrides[get_admin_user] = _get_admin_user

    with TestClient(app) as client:
        question_service.get_all_questions.return_value = mock_questions_list

        response = client.get("/question")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        question_service.get_all_questions.assert_called_once()
        
def test_get_question_by_id(client, question_service):
    question_service.get_question.return_value = mock_question

    response = client.get("/question/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    question_service.get_question.assert_called_once_with(1)

def test_get_nonexistent_question(client, question_service):
    question_service.get_question.return_value = None

    response = client.get("/question/999")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}
    question_service.get_question.assert_called_once_with(999)

def test_get_full_question(client, question_service):
    question_service.get_full_question.return_value = mock_full_question

    response = client.get("/question/1/full")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "answers" in data
    assert len(data["answers"]) == 1
    question_service.get_full_question.assert_called_once_with(1)

def test_update_question(client, question_service):
    updated_question = mock_question.model_copy()
    updated_question.title = "Updated Question"
    updated_question.description = "This is an updated question"
    question_service.update_question.return_value = updated_question

    response = client.put("/question/1", json={"title": updated_question.title, "description": updated_question.description})
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_question.title
    assert data["description"] == updated_question.description
    question_service.update_question.assert_called_once_with(1, QuestionCreate(title=updated_question.title, description=updated_question.description), 1)

def test_add_answer(client, question_service):
    question_service.add_answer.return_value = mock_answer

    response = client.post("/question/1/answer", json={"content": "This is an answer"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "This is an answer"
    assert data["question_id"] == 1
    question_service.add_answer.assert_called_once_with(AnswerCreate(content="This is an answer"), 1, 1)

def test_get_answers(client, question_service):
    question_service.get_answers.return_value = mock_full_question.answers

    response = client.get("/question/1/answers")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    question_service.get_answers.assert_called_once_with(1)

