# from pytest_mock import mocker
# from qna_api.questions.service import create_question, get_question, get_all_questions
# from qna_api.questions.models import QuestionCreate
# from qna_api.domain.user import UserEntity

# def test_create_question(mock_db_session):
#     mock_user = UserEntity(username="testuser", email="testuser@example.com", full_name="Test User", hashed_password="hashedpassword")
#     mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

#     question_data = QuestionCreate(title="Sample Question", description="This is a sample question")
#     question = create_question(mock_db_session, question_data, mock_user.id)
#     assert question.title == "Sample Question"
#     assert question.description == "This is a sample question"

# def test_get_question(mock_db_session):
#     mock_question = mocker.Mock()
#     mock_question.id = 1
#     mock_db_session.query.return_value.filter.return_value.first.return_value = mock_question

#     question = get_question(mock_db_session, 1)
#     assert question
#     assert question.id == 1

# def test_get_all_questions(mock_db_session):
#     mock_question = mocker.Mock()
#     mock_question.id = 1
#     mock_db_session.query.return_value.all.return_value = [mock_question]

#     questions = get_all_questions(mock_db_session)
#     assert isinstance(questions, list)
#     assert len(questions) > 0
