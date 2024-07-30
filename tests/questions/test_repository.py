import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from qna_api.domain.question import QuestionEntity
from qna_api.domain.answer import AnswerEntity
from qna_api.domain.user import UserEntity
from qna_api.questions.repository import QuestionRepository

# Mock data
mock_user = UserEntity(id=1, username="testuser", full_name="Test User", email="test@example.com", disabled=False, roles=["user"], questions=[], answers=[])
mock_answer = AnswerEntity(id=1, content="This is an answer", question_id=1, user_id=1)
mock_question = QuestionEntity(id=1, title="Sample Question", description="This is a sample question", user_id=1, 
                               user=mock_user, answers=[mock_answer])

@pytest.fixture
def db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def question_repository(db_session):
    return QuestionRepository(db=db_session)

def test_instance_method(db_session):
    with patch('qna_api.questions.repository.get_db', return_value=iter([db_session])):
        instance1 = QuestionRepository.instance()
        instance2 = QuestionRepository.instance()

        assert instance1 is instance2
        assert isinstance(instance1, QuestionRepository)
        assert instance1.db == db_session

        # Reset the singleton instance for other tests
        QuestionRepository._instance = None

def test_get_full_question(question_repository, db_session):
    query_mock = db_session.query().options().filter()
    query_mock.first.return_value = mock_question

    result = question_repository.get_full_question(1)

    assert result == mock_question

def test_add_answer(question_repository, db_session):
    db_session.add.return_value = None
    db_session.commit.return_value = None
    db_session.refresh.return_value = None

    result = question_repository.add_answer(mock_answer)

    assert result == mock_answer

def test_get_answers(question_repository, db_session):
    db_session.query().filter().all.return_value = [mock_answer]

    result = question_repository.get_answers(1)

    assert result == [mock_answer]
