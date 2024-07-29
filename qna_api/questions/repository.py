from sqlalchemy.orm import Session
from qna_api.questions.models import QuestionCreate, QuestionResponse
from qna_api.domain.question import QuestionEntity
from typing import List

class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, question: QuestionCreate, user_id: int) -> QuestionResponse:
        db_question = QuestionEntity(**question.model_dump(), user_id=user_id)
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return db_question

    def get_all(self) -> List[QuestionResponse]:
        return self.db.query(QuestionEntity).all()

    def get(self, question_id: int) -> QuestionResponse:
        return self.db.query(QuestionEntity).filter(QuestionEntity.id == question_id).first()
