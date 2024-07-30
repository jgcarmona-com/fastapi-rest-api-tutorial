from fastapi import APIRouter, Depends, HTTPException, status
from mediatr import Mediator
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.answers.service import AnswerService
from qna_api.auth.authorization import get_admin_user, get_authenticated_user
from qna_api.core.logging import get_logger
from qna_api.questions.commands.create_question_command import CreateQuestionCommand
from qna_api.questions.commands.delete_question_command import DeleteQuestionCommand
from qna_api.questions.commands.update_question_command import UpdateQuestionCommand
from qna_api.questions.models import FullQuestionResponse, QuestionCreate, QuestionResponse
from qna_api.questions.queries.get_all_questions_query import GetAllQuestionsQuery
from qna_api.questions.queries.get_full_question_query import GetFullQuestionQuery
from qna_api.questions.queries.get_question_query import GetQuestionQuery
from qna_api.user.models import User
from typing import List

logger = get_logger(__name__)

class QuestionController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_model=List[QuestionResponse])(self.get_all_questions)
        self.router.post("/", response_model=QuestionResponse)(self.create_question)
        self.router.get("/{question_id}", response_model=QuestionResponse)(self.get_question)
        self.router.get("/{question_id}/full", response_model=FullQuestionResponse)(self.get_full_question)
        self.router.put("/{question_id}", response_model=QuestionResponse)(self.update_question)
        self.router.delete("/{question_id}", response_model=QuestionResponse)(self.delete_question)

        # self.router.post("/{question_id}/answer", response_model=AnswerResponse)(self.add_answer)
        # self.router.get("/{question_id}/answers", response_model=List[AnswerResponse])(self.get_question_answers)

    async def create_question(self, question: QuestionCreate, current_user: User = Depends(get_authenticated_user)):
        try:
            created_question = await self.mediator.send_async(CreateQuestionCommand(question, current_user.id))
            return QuestionResponse.model_validate(created_question, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_all_questions(self, current_user: User = Depends(get_admin_user)):
        try:
            questions = await self.mediator.send_async(GetAllQuestionsQuery())
            return [QuestionResponse.model_validate(q, from_attributes=True) for q in questions]
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_question(self, question_id: int, current_user: User = Depends(get_authenticated_user)):
        try:
            question = await self.mediator.send_async(GetQuestionQuery(question_id))
            return QuestionResponse.model_validate(question, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    async def get_full_question(self, question_id: int, current_user: User = Depends(get_authenticated_user)):
        try:
            question = await self.mediator.send_async(GetFullQuestionQuery(question_id))
            return FullQuestionResponse.model_validate(question, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    async def update_question(self, question_id: int, question: QuestionCreate, current_user: User = Depends(get_authenticated_user)):
        try:
            updated_question = await self.mediator.send_async(UpdateQuestionCommand(question_id, question, current_user.id))
            return QuestionResponse.model_validate(updated_question, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def delete_question(self, question_id: int, current_user: User = Depends(get_authenticated_user)):
        try:
            deleted_question = await self.mediator.send_async(DeleteQuestionCommand(question_id, current_user.id))
            return QuestionResponse.model_validate(deleted_question, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # async def add_answer(self, question_id: int, answer: AnswerCreate,  current_user: User = Depends(get_authenticated_user)):
    #     logger.info(f"{current_user.full_name} is creating an answer for question {question_id}")
    #     return self.question_service.add_answer(answer, current_user.id, question_id)

    # async def get_question_answers(self, question_id: int,  current_user: User = Depends(get_authenticated_user)):
    #     logger.info(f"{current_user.full_name} is getting answers for question {question_id}")
    #     return self.question_service.get_answers(question_id)
