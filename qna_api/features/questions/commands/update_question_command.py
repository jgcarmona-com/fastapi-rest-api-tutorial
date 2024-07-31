from mediatr import Mediator
from qna_api.features.questions.models import QuestionCreate, Question
from qna_api.features.questions.repository import QuestionRepository

class UpdateQuestionCommand:
    def __init__(self, question_id: int, question: QuestionCreate, user_id: int):
        self.question_id = question_id
        self.question = question
        self.user_id = user_id

@Mediator.handler
class UpdateQuestionCommandHandler:
    def __init__(self):
        self.question_repository = QuestionRepository.instance()

    def handle(self, request: UpdateQuestionCommand) -> Question:
        db_question = self.question_repository.update(request.question_id, request.question, request.user_id)
        if not db_question:
            raise ValueError("Question not found or not authorized to update")
        return Question.model_validate(db_question, from_attributes=True)
