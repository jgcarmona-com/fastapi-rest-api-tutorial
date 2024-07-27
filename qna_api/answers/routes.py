from fastapi import APIRouter, Depends, HTTPException
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.answers.services import get_answer, create_answer, get_answers_for_question
from qna_api.auth.models import User
from qna_api.auth.services import get_current_user
from qna_api.core.database import get_db
from qna_api.core.logging import get_logger
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

logger = get_logger(__name__)

@router.post("/", response_model=AnswerResponse)
def create_answer_endpoint(answer: AnswerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"{current_user.full_name} is creating an answer")
    return create_answer(db=db, answer=answer, user_id=current_user.id)

@router.get("/{question_id}/answers/", response_model=List[AnswerResponse])
def get_answers(question_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"{current_user.full_name} is getting answers for question {question_id}")
    return get_answers_for_question(db=db, question_id=question_id)
