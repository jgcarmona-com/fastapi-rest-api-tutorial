from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from qna_api.core.database import Base

# Modelos Pydantic
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    roles: str | None = None