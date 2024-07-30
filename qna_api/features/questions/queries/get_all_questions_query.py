from mediatr import Mediator
from qna_api.features.questions.models import QuestionResponse
from qna_api.features.questions.repository import QuestionRepository

class GetAllQuestionsQuery:
    pass

@Mediator.handler
class GetAllQuestionsQueryHandler:
    def __init__(self):
        self.question_repository = QuestionRepository.instance()

    def handle(self, request: GetAllQuestionsQuery) -> list[QuestionResponse]:
        questions = self.question_repository.get_all()
        return [QuestionResponse.model_validate(q, from_attributes=True) for q in questions]
