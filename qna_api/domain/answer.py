from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from qna_api.core.database import Base

class AnswerEntity(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    question_id = Column(Integer, ForeignKey('questions.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    question = relationship("QuestionEntity", back_populates="answers")
    user = relationship("UserEntity", back_populates="answers")