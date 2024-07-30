from mediatr import Mediator
from qna_api.features.answers.models import AnswerResponse
from qna_api.features.questions.repository import QuestionRepository
from typing import List
from qna_api.core.logging import get_logger

logger = get_logger(__name__)

class GetQuestionAnswersQuery:
    def __init__(self, question_id: int):
        self.question_id = question_id

@Mediator.handler
class GetQuestionAnswersQueryHandler:
    def __init__(self):
        self.question_repository = QuestionRepository.instance()

    def handle(self, request: GetQuestionAnswersQuery) -> List[AnswerResponse]:
        logger.info(f"Getting answers for question {request.question_id}")
        answers = self.question_repository.get_answers(request.question_id)
        return [AnswerResponse.model_validate(answer, from_attributes=True) for answer in answers]
