from fastapi import APIRouter, Depends, HTTPException
from qna_api.auth.models import User
from qna_api.auth.services import get_current_user
from qna_api.core.database import get_db
from qna_api.core.logging import get_logger
from qna_api.questions.models import QuestionCreate, QuestionResponse
from qna_api.questions.services import get_question, create_question, get_all_questions
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

logger = get_logger(__name__)

@router.post("/", response_model=QuestionResponse)
def create_question_endpoint(question: QuestionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"{current_user.full_name} is creating a question")
    return create_question(db=db, question=question, user_id=current_user.id)

@router.get("/", response_model=List[QuestionResponse])
def get_questions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"{current_user.full_name} is getting all questions")
    return get_all_questions(db=db)

@router.get("/{question_id}", response_model=QuestionResponse)
def get_question_endpoint(question_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"{current_user.full_name} is getting question {question_id}")
    db_question = get_question(db, question_id=question_id)
    if db_question is None:
        logger.error(f"Question with id {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question
