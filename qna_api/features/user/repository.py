from sqlalchemy.orm import Session
from qna_api.core.base_repository import BaseRepository
from qna_api.domain.user import UserEntity
from qna_api.core.database import get_db

class UserRepository(BaseRepository[UserEntity]):
    def __init__(self, db: Session):
        super().__init__(UserEntity, db)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            db = next(get_db())
            cls._instance = cls(db)
        return cls._instance
    
    def get_by_username(self, username: str) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.username == username).first()