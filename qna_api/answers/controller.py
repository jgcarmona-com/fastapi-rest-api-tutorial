from fastapi import APIRouter, Depends, HTTPException, status
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.answers.service import AnswerService
from qna_api.auth.authorization import get_authenticated_user
from qna_api.core.logging import get_logger
from qna_api.user.models import User

logger = get_logger(__name__)

class AnswerController:
    def __init__(self, answer_service: AnswerService):
        self.answer_service = answer_service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/{answer_id}", response_model=AnswerResponse)(self.get_answer)
        self.router.put("/{answer_id}", response_model=AnswerResponse)(self.update_answer)
        self.router.delete("/{answer_id}", response_model=AnswerResponse)(self.delete_answer)

    async def get_answer(self, answer_id: int, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is getting answer {answer_id}")
        answer = self.answer_service.get_answer(answer_id)
        if not answer:
            logger.error(f"Answer with id {answer_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
        return answer

    async def update_answer(self, answer_id: int, answer: AnswerCreate, current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is updating answer {answer_id}")
        return self.answer_service.update_answer(answer_id, answer)

    async def delete_answer(self, answer_id: int,  current_user: User = Depends(get_authenticated_user)):
        logger.info(f"{current_user.full_name} is deleting answer {answer_id}")
        return self.answer_service.delete_answer(answer_id)
