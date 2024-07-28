from fastapi import APIRouter, Depends, HTTPException
from typing import List
from qna_api.auth.service import AuthService
from qna_api.auth.models import User
from qna_api.core.logging import get_logger
from qna_api.questions.models import QuestionCreate, QuestionResponse
from qna_api.questions.service import QuestionService

logger = get_logger(__name__)

class QuestionController:
    def __init__(self, question_service: QuestionService, auth_service: AuthService):
        self.question_service = question_service
        self.auth_service = auth_service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", response_model=QuestionResponse)(self.create_question)
        self.router.get("/", response_model=List[QuestionResponse])(self.get_questions)
        self.router.get("/{question_id}", response_model=QuestionResponse)(self.get_question)

    async def create_question(self, question: QuestionCreate, token: str = Depends(AuthService.oauth2_scheme)):
        current_user = self.auth_service.get_current_user(token)
        logger.info(f"{current_user.full_name} is creating a question")
        return self.question_service.create_question(question=question, user_id=current_user.id)

    async def get_questions(self, token: str = Depends(AuthService.oauth2_scheme)):
        current_user = self.auth_service.get_current_user(token)
        logger.info(f"{current_user.full_name} is getting all questions")
        return self.question_service.get_all_questions()

    async def get_question(self, question_id: int, token: str = Depends(AuthService.oauth2_scheme)):
        current_user = self.auth_service.get_current_user(token)
        logger.info(f"{current_user.full_name} is getting question {question_id}")
        question = self.question_service.get_question(question_id=question_id)
        if question is None:
            logger.error(f"Question with id {question_id} not found")
            raise HTTPException(status_code=404, detail="Question not found")
        return question
