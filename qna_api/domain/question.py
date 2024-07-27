from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from qna_api.core.database import Base

class QuestionEntity(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("UserEntity", back_populates="questions")
    answers = relationship("AnswerEntity", back_populates="question")
