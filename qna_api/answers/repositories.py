from sqlalchemy.orm import Session
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.domain.answer import AnswerEntity
from typing import List

class AnswerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, answer: AnswerCreate, user_id: int) -> AnswerResponse:
        db_answer = AnswerEntity(**answer.dict(), user_id=user_id)
        self.db.add(db_answer)
        self.db.commit()
        self.db.refresh(db_answer)
        return db_answer

    def get_by_question_id(self, question_id: int) -> List[AnswerResponse]:
        return self.db.query(AnswerEntity).filter(AnswerEntity.question_id == question_id).all()

    def get(self, answer_id: int) -> AnswerResponse:
        return self.db.query(AnswerEntity).filter(AnswerEntity.id == answer_id).first()
