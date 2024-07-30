from mediatr import Mediator
from qna_api.features.questions.models import QuestionResponse
from qna_api.features.questions.repository import QuestionRepository

class GetQuestionQuery:
    def __init__(self, question_id: int):
        self.question_id = question_id

@Mediator.handler
class GetQuestionQueryHandler:
    def __init__(self):
        self.question_repository = QuestionRepository.instance()

    def handle(self, request: GetQuestionQuery) -> QuestionResponse:
        question = self.question_repository.get(request.question_id)
        if not question:
            raise ValueError("Question not found")
        return QuestionResponse.model_validate(question, from_attributes=True)
