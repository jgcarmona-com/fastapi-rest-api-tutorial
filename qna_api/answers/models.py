from pydantic import BaseModel, Field

class AnswerBase(BaseModel):
    content: str = Field(..., example="You can implement authentication in FastAPI using JWT by following these steps...")

class AnswerCreate(AnswerBase):
    question_id: int

class AnswerResponse(AnswerBase):
    id: int
    question_id: int
    user_id: int

    class Config:
        from_attributes = True