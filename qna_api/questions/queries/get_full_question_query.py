from mediatr import Mediator
from qna_api.questions.models import FullQuestionResponse
from qna_api.questions.repository import QuestionRepository

class GetFullQuestionQuery:
    def __init__(self, question_id: int):
        self.question_id = question_id

@Mediator.handler
class GetFullQuestionQueryHandler:
    def __init__(self):
        self.question_repository = QuestionRepository.instance()

    def handle(self, request: GetFullQuestionQuery) -> FullQuestionResponse:
        question = self.question_repository.get_full_question(request.question_id)
        if not question:
            raise ValueError("Question not found")
        return FullQuestionResponse.model_validate(question, from_attributes=True)
