# qna_api/features/answers/controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from mediatr import Mediator
from qna_api.features.answers.models import AnswerCreate, AnswerUpdate, AnswerResponse
from qna_api.crosscutting.authorization import get_authenticated_user
from qna_api.crosscutting.logging import get_logger
from qna_api.features.user.models import User
from qna_api.features.answers.queries.get_answer_query import GetAnswerQuery
from qna_api.features.answers.commands.update_answer_command import UpdateAnswerCommand
from qna_api.features.answers.commands.delete_answer_command import DeleteAnswerCommand
from qna_api.features.answers.commands.add_answer_command import AddAnswerCommand
from qna_api.features.answers.queries.get_question_answers_query import GetQuestionAnswersQuery
from typing import List

logger = get_logger(__name__)

class AnswerController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/{question_id}/answer/{answer_id}", response_model=AnswerResponse)(self.get_answer)
        self.router.put("/{question_id}/answer/{answer_id}", response_model=AnswerResponse)(self.update_answer)
        self.router.delete("/{question_id}/answer/{answer_id}", response_model=AnswerResponse)(self.delete_answer)
        self.router.post("/{question_id}/answer", response_model=AnswerResponse)(self.add_answer)
        self.router.get("/{question_id}/answers", response_model=List[AnswerResponse])(self.get_question_answers)

    async def get_answer(self, question_id: int, answer_id: int, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is getting answer {answer_id} for question {question_id}")
        try:
            answer = await self.mediator.send_async(GetAnswerQuery(answer_id))
            return answer
        except ValueError as e:
            logger.error(f"Answer with id {answer_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    async def update_answer(self, question_id: int, answer_id: int, answer: AnswerUpdate, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is updating answer {answer_id} for question {question_id}")
        try:
            return await self.mediator.send_async(UpdateAnswerCommand(answer_id, answer))
        except ValueError as e:
            logger.error(f"Error updating answer: {str(e)}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    async def delete_answer(self, question_id: int, answer_id: int, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is deleting answer {answer_id} for question {question_id}")
        try:
            return await self.mediator.send_async(DeleteAnswerCommand(answer_id))
        except ValueError as e:
            logger.error(f"Error deleting answer: {str(e)}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    async def add_answer(self, question_id: int, answer: AnswerCreate, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is creating an answer for question {question_id}")
        try:
            created_answer = await self.mediator.send_async(AddAnswerCommand(question_id, answer, current_user.id))
            return AnswerResponse.model_validate(created_answer, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_question_answers(self, question_id: int, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is getting answers for question {question_id}")
        try:
            answers = await self.mediator.send_async(GetQuestionAnswersQuery(question_id))
            return [AnswerResponse.model_validate(answer, from_attributes=True) for answer in answers]
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
