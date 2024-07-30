from mediatr import Mediator
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.domain.answer import AnswerEntity
from qna_api.questions.repository import QuestionRepository
from qna_api.core.logging import get_logger

logger = get_logger(__name__)

class AddAnswerCommand:
    def __init__(self, question_id: int, answer: AnswerCreate, user_id: int):
        self.question_id = question_id
        self.answer = answer
        self.user_id = user_id

@Mediator.handler
class AddAnswerCommandHandler:
    def __init__(self):
        self.question_repository = QuestionRepository.instance()

    def handle(self, request: AddAnswerCommand) -> AnswerResponse:
        logger.info(f"User {request.user_id} is adding an answer to question {request.question_id}")
        db_answer = AnswerEntity(
            content=request.answer.content,
            user_id=request.user_id,
            question_id=request.question_id
        )
        self.question_repository.add_answer(db_answer)
        return AnswerResponse.model_validate(db_answer, from_attributes=True)
