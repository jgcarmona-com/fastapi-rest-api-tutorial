from fastapi import APIRouter, Depends, HTTPException, status
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.answers.service import AnswerService
from qna_api.auth.service import AuthService, get_authenticated_user
from qna_api.core.logging import get_logger
from qna_api.questions.models import FullQuestionResponse, QuestionCreate, QuestionResponse
from qna_api.questions.service import QuestionService
from qna_api.user.models import User
from typing import List

logger = get_logger(__name__)

class QuestionController:
    def __init__(self, question_service: QuestionService, answer_service: AnswerService):
        self.question_service = question_service
        self.answer_service = answer_service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/all", response_model=List[QuestionResponse])(self.get_all_questions)
        self.router.post("/", response_model=QuestionResponse)(self.create_question)
        self.router.get("/{question_id}", response_model=QuestionResponse)(self.get_question)
        self.router.get("/{question_id}/full", response_model=FullQuestionResponse)(self.get_full_question)
        self.router.put("/{question_id}", response_model=QuestionResponse)(self.update_question)
        self.router.delete("/{question_id}", response_model=QuestionResponse)(self.delete_question)

        self.router.post("/{question_id}/answer", response_model=AnswerResponse)(self.create_answer)
        self.router.get("/{question_id}/answers", response_model=List[AnswerResponse])(self.get_answers)

    async def create_question(self, question: QuestionCreate, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is creating a question")
        return self.question_service.create_question(question, current_user.id)

    async def get_all_questions(self, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is getting all questions")
        return self.question_service.get_all_questions()

    async def get_question(self, question_id: int, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is getting question {question_id}")
        question = self.question_service.get_question(question_id)
        if not question:
            logger.error(f"Question with id {question_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        return question
    
    async def get_full_question(self, question_id: int, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is getting full question {question_id}")
        question = self.question_service.get_full_question(question_id)
        if not question:
            logger.error(f"Question with id {question_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        return question

    async def update_question(self, question_id: int, question: QuestionCreate, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is updating question {question_id}")
        return self.question_service.update_question(question_id, question, current_user.id)

    async def delete_question(self, question_id: int, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is deleting question {question_id}")
        return self.question_service.delete_question(question_id, current_user.id)

    async def create_answer(self, question_id: int, answer: AnswerCreate,  current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is creating an answer for question {question_id}")
        return self.answer_service.create_answer(answer, current_user.id, question_id)

    async def get_answers(self, question_id: int,  current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is getting answers for question {question_id}")
        return self.answer_service.get_answers_for_question(question_id)
