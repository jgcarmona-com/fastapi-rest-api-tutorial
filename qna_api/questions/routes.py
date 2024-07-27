from fastapi import APIRouter, Depends, HTTPException
from qna_api.auth.services import AuthService
from qna_api.core.logging import get_logger
from qna_api.questions.models import QuestionCreate, QuestionResponse
from qna_api.questions.services import QuestionsService
from typing import List

logger = get_logger(__name__)

class QuestionsController:
    def __init__(self, questions_service: QuestionsService, auth_service: AuthService):
        self.questions_service = questions_service
        self.auth_service = auth_service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", response_model=QuestionResponse)(self.create_question_endpoint)
        self.router.get("/", response_model=List[QuestionResponse])(self.get_questions)
        self.router.get("/{question_id}", response_model=QuestionResponse)(self.get_question_endpoint)

    def create_question_endpoint(self, question: QuestionCreate, token: str = Depends(AuthService.oauth2_scheme)):
        current_user = self.auth_service.get_current_user(token)
        logger.info(f"{current_user.full_name} is creating a question")
        return self.questions_service.create_question(question=question, user_id=current_user.id)

    def get_questions(self, token: str = Depends(AuthService.oauth2_scheme)):
        current_user = self.auth_service.get_current_user(token)
        logger.info(f"{current_user.full_name} is getting all questions")
        return self.questions_service.get_all_questions()

    def get_question_endpoint(self, question_id: int, token: str = Depends(AuthService.oauth2_scheme)):
        current_user = self.auth_service.get_current_user(token)
        logger.info(f"{current_user.full_name} is getting question {question_id}")
        db_question = self.questions_service.get_question(question_id=question_id)
        if db_question is None:
            logger.error(f"Question with id {question_id} not found")
            raise HTTPException(status_code=404, detail="Question not found")
        return db_question
