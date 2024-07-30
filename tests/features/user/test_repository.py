import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from qna_api.domain.question import QuestionEntity
from qna_api.domain.answer import AnswerEntity
from qna_api.domain.user import UserEntity
from qna_api.features.user.repository import UserRepository

# Mock data
mock_answer = AnswerEntity(id=1, content="This is an answer", question_id=1, user_id=1)
mock_question = QuestionEntity(id=1, title="Sample Question", description="This is a sample question", user_id=1, answers=[mock_answer])
mock_user = UserEntity(id=1, username="testuser", full_name="Test User", email="test@example.com", disabled=False, roles=["user"], questions=[mock_question], answers=[mock_answer])

@pytest.fixture
def db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def user_repository(db_session):
    return UserRepository(db=db_session)

def test_instance_method(db_session):
    with patch('qna_api.features.user.repository.get_db', return_value=iter([db_session])):
        # Reset the singleton instance for other tests
        UserRepository._instance = None
        instance1 = UserRepository.instance()
        instance2 = UserRepository.instance()

        assert instance1 is instance2
        assert isinstance(instance1, UserRepository)
        assert instance1.db == db_session

        # Reset the singleton instance for other tests
        UserRepository._instance = None

def test_get_by_username(user_repository, db_session):
    db_session.query().filter().first.return_value = mock_user

    result = user_repository.get_by_username("testuser")

    assert result == mock_user