from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    id: int | None = None
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        from_attributes = True

class UserCreate(User):
    password: str

class UserUpdate(User):
    password: str | None = None
