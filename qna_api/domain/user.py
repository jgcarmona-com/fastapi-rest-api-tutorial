from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from qna_api.core.database import Base

class UserEntity(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    questions = relationship("QuestionEntity", back_populates="user")
    answers = relationship("AnswerEntity", back_populates="user")
