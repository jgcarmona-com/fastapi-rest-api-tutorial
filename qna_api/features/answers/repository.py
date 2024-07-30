from sqlalchemy.orm import Session
from qna_api.core.base_repository import BaseRepository
from qna_api.domain.answer import AnswerEntity
from qna_api.core.database import get_db

class AnswerRepository(BaseRepository[AnswerEntity]):
    def __init__(self, db: Session):
        super().__init__(AnswerEntity, db)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            db = next(get_db())
            cls._instance = cls(db)
        return cls._instance