from qna_api.features.answers.models import Answer

mock_answer = Answer(
    id=1,
    content="This is an answer",
    question_id=1,
    user_id=1
)

mock_updated_answer = Answer(
    id=1,
    content="This is an updated answer",
    question_id=1,
    user_id=1
)

