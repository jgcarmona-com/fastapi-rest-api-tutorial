from fastapi import APIRouter, Depends
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.auth.services import AuthService
from qna_api.core.logging import get_logger
from qna_api.answers.services import AnswersService
from typing import List

logger = get_logger(__name__)

class AnswersController:
    def __init__(self, answers_service: AnswersService, auth_service: AuthService):
        self.answers_service = answers_service
        self.auth_service = auth_service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", response_model=AnswerResponse)(self.create_answer_endpoint)
        self.router.get("/{question_id}/answers/", response_model=List[AnswerResponse])(self.get_answers)

    def create_answer_endpoint(self, answer: AnswerCreate, token: str = Depends(AuthService.oauth2_scheme)):
        current_user = self.auth_service.get_current_user(token)
        logger.info(f"{current_user.full_name} is creating an answer")
        return self.answers_service.create_answer(answer=answer, user_id=current_user.id)

    def get_answers(self, question_id: int, token: str = Depends(AuthService.oauth2_scheme)):
        current_user = self.auth_service.get_current_user(token)
        logger.info(f"{current_user.full_name} is getting answers for question {question_id}")
        return self.answers_service.get_answers_for_question(question_id)
