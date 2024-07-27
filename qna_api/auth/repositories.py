from sqlalchemy.orm import Session
from qna_api.domain.user import UserEntity

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserEntity) -> UserEntity:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_username(self, username: str) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.username == username).first()
