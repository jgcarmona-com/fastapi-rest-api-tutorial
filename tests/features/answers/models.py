from qna_api.features.answers.models import AnswerResponse

mock_answer = AnswerResponse(
    id=1,
    content="This is an answer",
    question_id=1,
    user_id=1
)

mock_updated_answer = AnswerResponse(
    id=1,
    content="This is an updated answer",
    question_id=1,
    user_id=1
)

