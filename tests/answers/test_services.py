# from pytest_mock import mocker
# from qna_api.answers.services import create_answer, get_answers_for_question
# from qna_api.answers.models import AnswerCreate
# from qna_api.domain.user import UserEntity
# from qna_api.domain.question import QuestionEntity

# def test_create_answer(mock_db_session):
#     mock_user = UserEntity(username="testuser", email="testuser@example.com", full_name="Test User", hashed_password="hashedpassword")
#     mock_question = QuestionEntity(title="Sample Question", description="This is a sample question", user_id=mock_user.id)

#     mock_db_session.query.return_value.filter.return_value.first.side_effect = [mock_user, mock_question]

#     answer_data = AnswerCreate(question_id=mock_question.id, content="This is a sample answer")
#     answer = create_answer(mock_db_session, answer_data, mock_user.id)
#     assert answer.content == "This is a sample answer"
#     assert answer.question_id == mock_question.id

# def test_get_answers_for_question(mock_db_session):
#     mock_answer = mocker.Mock()
#     mock_answer.id = 1
#     mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_answer]

#     answers = get_answers_for_question(mock_db_session, 1)
#     assert isinstance(answers, list)
#     assert len(answers) > 0
