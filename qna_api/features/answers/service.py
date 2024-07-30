from sqlalchemy.orm import Session
from qna_api.features.answers.models import AnswerCreate, AnswerResponse
from qna_api.domain.answer import AnswerEntity

class AnswerService:
    def __init__(self, db: Session):
        self.db = db

    def get_answer(self, answer_id: int) -> AnswerResponse:
        db_answer = self.db.query(AnswerEntity).filter(AnswerEntity.id == answer_id).first()
        if db_answer is None:
            return None
        return AnswerResponse.model_validate(db_answer)

    def update_answer(self, answer_id: int, answer: AnswerCreate, user_id: int) -> AnswerResponse:
        db_answer = self.db.query(AnswerEntity).filter(AnswerEntity.id == answer_id, AnswerEntity.user_id == user_id).first()
        if db_answer is None:
            return None
        for key, value in answer.dict().items():
            setattr(db_answer, key, value)
        self.db.commit()
        self.db.refresh(db_answer)
        return AnswerResponse.model_validate(db_answer)

    def delete_answer(self, answer_id: int, user_id: int) -> AnswerResponse:
        db_answer = self.db.query(AnswerEntity).filter(AnswerEntity.id == answer_id, AnswerEntity.user_id == user_id).first()
        if db_answer is None:
            return None
        self.db.delete(db_answer)
        self.db.commit()
        return AnswerResponse.model_validate(db_answer)
