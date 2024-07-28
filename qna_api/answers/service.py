from sqlalchemy.orm import Session
from qna_api.answers.models import AnswerCreate, AnswerResponse
from qna_api.domain.answer import AnswerEntity

class AnswerService:
    def __init__(self, db: Session):
        self.db = db

    def create_answer(self, answer: AnswerCreate, user_id: int, question_id: int) -> AnswerResponse:
        db_answer = AnswerEntity(
            content=answer.content,
            user_id=user_id,
            question_id=question_id
        )
        self.db.add(db_answer)
        self.db.commit()
        self.db.refresh(db_answer)
        return AnswerResponse.model_validate(db_answer)

    def get_answer(self, answer_id: int) -> AnswerResponse:
        db_answer = self.db.query(AnswerEntity).filter(AnswerEntity.id == answer_id).first()
        if db_answer is None:
            return None
        return AnswerResponse.model_validate(db_answer)

    def get_answers_for_question(self, question_id: int) -> list[AnswerResponse]:
        answers = self.db.query(AnswerEntity).filter(AnswerEntity.question_id == question_id).all()
        return [AnswerResponse.model_validate(a) for a in answers]

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
