from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from qna_api.core.database import Base

# Modelos Pydantic
class QuestionBase(BaseModel):
    title: str = Field(..., example="How to implement authentication in FastAPI?")
    description: str = Field(..., example="I need help with implementing authentication using JWT in FastAPI.")

    @field_validator('description')
    def validate_description(cls, v):
        if len(v) < 10:
            raise ValueError('Description must be at least 10 characters long')
        if len(v) > 200:
            raise ValueError('Description must be less than 200 characters')
        return v

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
