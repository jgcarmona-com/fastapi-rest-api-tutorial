from mediatr import Mediator
from qna_api.features.answers.repository import AnswerRepository
from qna_api.features.answers.models import AnswerUpdate, AnswerResponse
from qna_api.crosscutting.logging import get_logger

logger = get_logger(__name__)

class UpdateAnswerCommand:
    def __init__(self, answer_id: int, answer: AnswerUpdate):
        self.answer_id = answer_id
        self.answer = answer

@Mediator.handler
class UpdateAnswerCommandHandler:
    def __init__(self):
        self.answer_repository = AnswerRepository.instance()

    def handle(self, command: UpdateAnswerCommand) -> AnswerResponse:
        logger.info(f"Updating answer {command.answer_id}")
        answer = self.answer_repository.get(command.answer_id)
        if not answer:
            raise ValueError(f"Answer with id {command.answer_id} not found")
        
        answer.content = command.answer.content
        self.answer_repository.update(answer)
        logger.info(f"Answer {command.answer_id} updated")
        return answer
