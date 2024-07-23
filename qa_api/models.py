from pydantic import BaseModel
from typing import Optional

# DTOs
class Question(BaseModel):
    title: str
    description: str

class QuestionResponse(Question):
    id: Optional[int]

class Answer(BaseModel):
    question_id: int
    content: str

class AnswerResponse(Answer):
    id: Optional[int]

class Comment(BaseModel):
    answer_id: int
    content: str

class CommentResponse(Comment):
    id: Optional[int]

# DOMAIN ENTITIES:
class QuestionEntity(BaseModel):
    id: int
    title: str
    description: str

class AnswerEntity(BaseModel):
    id: int
    question_id: int
    content: str

class CommentEntity(BaseModel):
    id: int
    answer_id: int
    content: str
