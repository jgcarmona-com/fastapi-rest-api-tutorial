from mediatr import Mediator
from qna_api.features.questions.models import QuestionResponse
from qna_api.features.questions.repository import QuestionRepository

class DeleteQuestionCommand:
    def __init__(self, question_id: int, user_id: int):
        self.question_id = question_id
        self.user_id = user_id

@Mediator.handler
class DeleteQuestionCommandHandler:
    def __init__(self):
        self.question_repository = QuestionRepository.instance()

    def handle(self, request: DeleteQuestionCommand) -> QuestionResponse:
        db_question = self.question_repository.delete(request.question_id, request.user_id)
        if not db_question:
            raise ValueError("Question not found or not authorized to delete")
        return QuestionResponse.model_validate(db_question, from_attributes=True)
