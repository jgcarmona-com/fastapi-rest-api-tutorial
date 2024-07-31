from mediatr import Mediator
from qna_api.features.answers.repository import AnswerRepository
from qna_api.features.answers.models import Answer

from qna_api.crosscutting.logging import get_logger

logger = get_logger(__name__)

class DeleteAnswerCommand:
    def __init__(self, answer_id: int):
        self.answer_id = answer_id

@Mediator.handler
class DeleteAnswerCommandHandler:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    def handle(self, command: DeleteAnswerCommand) -> Answer:
        logger.info(f"Deleting answer {command.answer_id}")
        answer = self.answer_repository.get(command.answer_id)
        if not answer:
            raise ValueError(f"Answer with id {command.answer_id} not found")
        
        self.answer_repository.delete(command.answer_id)
        logger.info(f"Answer {command.answer_id} deleted")
        return answer
