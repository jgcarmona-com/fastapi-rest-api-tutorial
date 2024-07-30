from sqlalchemy.orm import Session, joinedload
from qna_api.core.base_repository import BaseRepository
from qna_api.core.database import get_db
from qna_api.domain.question import QuestionEntity
from qna_api.domain.answer import AnswerEntity
from typing import List

class QuestionRepository(BaseRepository[QuestionEntity]):
    def __init__(self, db: Session):
        super().__init__(QuestionEntity, db)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            db = next(get_db())
            cls._instance = cls(db)
        return cls._instance

    def get_full_question(self, question_id: int) -> QuestionEntity:
        db_question = (
            self.db.query(QuestionEntity)
            .options(
                joinedload(QuestionEntity.answers),
                joinedload(QuestionEntity.user),
                joinedload(QuestionEntity.answers).joinedload(AnswerEntity.user)
            )
            .filter(QuestionEntity.id == question_id)
            .first()
        )
        return db_question

    def add_answer(self, answer: AnswerEntity) -> AnswerEntity:
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer
    
    def get_answers(self, question_id: int) -> List[AnswerEntity]:
        return self.db.query(AnswerEntity).filter(AnswerEntity.question_id == question_id).all()