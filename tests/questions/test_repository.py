# import pytest
# from unittest.mock import MagicMock
# from sqlalchemy.orm import Session
# from qna_api.domain.question import QuestionEntity
# from qna_api.domain.answer import AnswerEntity
# from qna_api.questions.repository import QuestionRepository

# # Mock data
# mock_question = QuestionEntity(id=1, title="Sample Question", description="This is a sample question", user_id=1)
# mock_answer = AnswerEntity(id=1, content="This is an answer", question_id=1, user_id=1)

# @pytest.fixture
# def db_session():
#     return MagicMock(spec=Session)

# @pytest.fixture
# def question_repository(db_session):
#     return QuestionRepository(db=db_session)

# def test_get_full_question(question_repository, db_session):
#     db_session.query().options().filter().first.return_value = mock_question

#     result = question_repository.get_full_question(1)

#     assert result == mock_question
#     db_session.query().options().filter().first.assert_called_once()

# def test_add_answer(question_repository, db_session):
#     db_session.add.return_value = None
#     db_session.commit.return_value = None
#     db_session.refresh.return_value = None

#     result = question_repository.add_answer(mock_answer)

#     assert result == mock_answer
#     db_session.add.assert_called_once_with(mock_answer)
#     db_session.commit.assert_called_once()
#     db_session.refresh.assert_called_once_with(mock_answer)

# def test_get_answers(question_repository, db_session):
#     db_session.query().filter().all.return_value = [mock_answer]

#     result = question_repository.get_answers(1)

#     assert result == [mock_answer]
#     db_session.query().filter().all.assert_called_once()
