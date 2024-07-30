from sqlalchemy.orm import Session
from qna_api.core.base_repository import BaseRepository
from qna_api.domain.vote import VoteEntity
from qna_api.core.database import get_db

class VoteRepository(BaseRepository[VoteEntity]):
    def __init__(self, db: Session):
        super().__init__(VoteEntity, db)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            db = next(get_db())
            cls._instance = cls(db)
        return cls._instance
