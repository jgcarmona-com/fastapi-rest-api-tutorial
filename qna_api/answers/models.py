from pydantic import BaseModel

class AnswerCreate(BaseModel):
    content: str

class AnswerResponse(BaseModel):
    id: int
    content: str
    question_id: int
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True # This is required to convert SQLAlchemy objects to Pydantic models
