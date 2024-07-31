from pydantic import BaseModel

class AnswerCreate(BaseModel):
    content: str

class AnswerUpdate(BaseModel):
    content: str

class Answer(BaseModel):
    id: int
    content: str
    question_id: int
    user_id: int

    class Config:
        from_attributes = True
