from qna_api.features.questions.models import QuestionResponse, FullQuestionResponse
from qna_api.features.answers.models import AnswerResponse

# Some useful mock data
mock_question = QuestionResponse(
    id=1,
    title="Sample Question",
    description="This is a sample question",
    user_id=1,
    answers=[],
    
)

mock_answer = AnswerResponse(
    id=1, 
    question_id=1, 
    user_id=1, 
    content="This is an answer"
)

mock_full_question = FullQuestionResponse(
    id=1,
    title="Sample Question",
    description="This is a sample question",
    user_id=1,
    answers=[
        mock_answer
    ]
)

mock_questions_list = [mock_question]
