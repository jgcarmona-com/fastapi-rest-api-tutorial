from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from qna_api.core.database import Base

# Modelos Pydantic
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: bool | None = None

    class Config:
        from_attributes = True