from sqlalchemy import Column, Enum, Integer, String, Boolean
from sqlalchemy.orm import relationship
from qna_api.core.database import Base
from qna_api.domain.role import Role

class UserEntity(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    role = Column(Enum(Role), default=Role.USER)

    questions = relationship("QuestionEntity", back_populates="user")
    answers = relationship("AnswerEntity", back_populates="user")
