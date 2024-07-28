from pydantic import BaseModel, EmailStr

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

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    full_name: str = None
    disabled: bool = None
    password: str = None

class User(UserBase):
    id: int
    disabled: bool | None = None

    class Config:
        from_attributes = True