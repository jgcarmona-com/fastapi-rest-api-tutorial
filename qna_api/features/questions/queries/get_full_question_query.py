from mediatr import Mediator
from qna_api.features.questions.models import FullQuestion
from qna_api.features.questions.repository import QuestionRepository

class GetFullQuestionQuery:
    def __init__(self, question_id: int):
        self.question_id = question_id

@Mediator.handler
class GetFullQuestionQueryHandler:
    def __init__(self):
        self.question_repository = QuestionRepository.instance()

    def handle(self, request: GetFullQuestionQuery) -> FullQuestion:
        question = self.question_repository.get_full_question(request.question_id)
        if not question:
            raise ValueError("Question not found")
        return FullQuestion.model_validate(question, from_attributes=True)
