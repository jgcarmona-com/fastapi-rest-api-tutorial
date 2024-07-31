from qna_api.features.questions.models import Question, FullQuestion
from qna_api.features.answers.models import Answer

# Some useful mock data
mock_question = Question(
    id=1,
    title="Sample Question",
    description="This is a sample question",
    user_id=1,
    answers=[],
    
)

mock_answer = Answer(
    id=1, 
    question_id=1, 
    user_id=1, 
    content="This is an answer"
)

mock_full_question = FullQuestion(
    id=1,
    title="Sample Question",
    description="This is a sample question",
    user_id=1,
    answers=[
        mock_answer
    ]
)

mock_questions_list = [mock_question]
