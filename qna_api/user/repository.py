from sqlalchemy.orm import Session
from qna_api.domain.user import UserEntity
from qna_api.core.database import get_db

class UserRepository:
    _instance = None

    def __init__(self, db: Session):
        self.db = db

    @classmethod
    def instance(cls):
        if cls._instance is None:
            db = next(get_db())
            cls._instance = cls(db)
        return cls._instance

    def create(self, user: UserEntity) -> UserEntity:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get(self, question_id: int) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.id == question_id).first()
    
    def get_by_username(self, username: str) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.username == username).first()
