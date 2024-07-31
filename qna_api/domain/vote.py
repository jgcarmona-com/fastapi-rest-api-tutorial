from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from qna_api.core.database import Base

class VoteEntity(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=True)
    answer_id = Column(Integer, ForeignKey('answers.id'), nullable=True)
    vote_value = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("UserEntity")
    question = relationship("QuestionEntity")
    answer = relationship("AnswerEntity")
