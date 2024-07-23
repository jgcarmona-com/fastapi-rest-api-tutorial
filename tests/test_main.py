"""TEST QA API ENDPOINTS"""
from fastapi.testclient import TestClient
from qa_api.main import app
import pytest
from dotenv import load_dotenv

client = TestClient(app)

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

# # def test_redirect_to_swagger():
# #     """Tests redirect to Swagger endpoint"""
# #     response = client.get("/")
# #     assert response.status_code == 200
# #     assert response.url.endswith("/docs")

def test_create_question():
    """Tests creating a question"""
    response = client.post("/questions/", json={"title": "Sample Question", "description": "This is a sample question"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Sample Question", "description": "This is a sample question"}

def test_get_questions():
    """Tests fetching all questions"""
    response = client.get("/questions/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "title": "Sample Question", "description": "This is a sample question"}]

def test_get_question_by_id():
    """Tests fetching a question by ID"""
    response = client.get("/questions/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Sample Question", "description": "This is a sample question"}

def test_get_nonexistent_question():
    """Tests fetching a non-existent question by ID"""
    response = client.get("/questions/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}

def test_create_question_with_invalid_body():
    """Tests creating a question with an invalid body"""
   
    invalid_bodies = [
        {"title": "Sample Question"},  # Descripction is Missing
        {"description": "This is a sample question"},  # Title is missing
        "invalid string instead of a dict"  # wrong body
    ]

    for invalid_body in invalid_bodies:
        response = client.post("/questions/", json=invalid_body)
        assert response.status_code == 422  # Unprocessable Entity
        assert response.json()["detail"] is not None  # Verify error message

def test_create_answer():
    """Tests creating an answer"""
    client.post("/questions/", json={"title": "Sample Question", "description": "This is a sample question"})
    response = client.post("/answers/", json={"question_id": 1, "content": "This is a sample answer"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "question_id": 1, "content": "This is a sample answer"}

def test_get_answers():
    """Tests fetching all answers for a question"""
    response = client.get("/questions/1/answers/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "question_id": 1, "content": "This is a sample answer"}]

def test_create_answer_with_invalid_body():
    """Tests creating an answer with an invalid body"""
    invalid_bodies = [
        {"content": "This is a sample answer"},  # Falta el question_id
        {"question_id": 1},  # Falta el content
        "invalid string instead of a dict"  # Totalmente incorrecto
    ]

    for invalid_body in invalid_bodies:
        response = client.post("/answers/", json=invalid_body)
        assert response.status_code == 422  # Unprocessable Entity
        assert response.json()["detail"] is not None  # Verificar que hay un mensaje de error

def test_create_comment():
    """Tests creating a comment"""
    client.post("/questions/", json={"title": "Sample Question", "description": "This is a sample question"})
    client.post("/answers/", json={"question_id": 1, "content": "This is a sample answer"})
    response = client.post("/comments/", json={"answer_id": 1, "content": "This is a sample comment"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "answer_id": 1, "content": "This is a sample comment"}

def test_get_comments():
    """Tests fetching all comments for an answer"""
    response = client.get("/answers/1/comments/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "answer_id": 1, "content": "This is a sample comment"}]

def test_create_comment_with_invalid_body():
    """Tests creating a comment with an invalid body"""
    invalid_bodies = [
        {"content": "This is a sample comment"},  # Falta el answer_id
        {"answer_id": 1},  # Falta el content
        "invalid string instead of a dict"  # Totalmente incorrecto
    ]

    for invalid_body in invalid_bodies:
        response = client.post("/comments/", json=invalid_body)
        assert response.status_code == 422  # Unprocessable Entity
        assert response.json()["detail"] is not None  # Verificar que hay un mensaje de error
