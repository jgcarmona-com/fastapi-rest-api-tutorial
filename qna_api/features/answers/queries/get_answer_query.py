from mediatr import Mediator
from qna_api.features.answers.repository import AnswerRepository
from qna_api.features.answers.models import AnswerResponse
from qna_api.crosscutting.logging import get_logger

logger = get_logger(__name__)

class GetAnswerQuery:
    def __init__(self, answer_id: int):
        self.answer_id = answer_id

@Mediator.handler
class GetAnswerQueryHandler:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    def handle(self, query: GetAnswerQuery) -> AnswerResponse:
        logger.info(f"Getting answer {query.answer_id}")
        answer = self.answer_repository.get(query.answer_id)
        if not answer:
            raise ValueError(f"Answer with id {query.answer_id} not found")
        return answer
