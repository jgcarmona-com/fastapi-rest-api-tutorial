from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from qna_api.auth.models import UserCreate, Token
from qna_api.auth.repositories import UserRepository
from qna_api.auth.services import AuthService
from qna_api.core.config import settings
from typing import List

class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/token", response_model=Token)(self.authenticate)
        self.router.post("/users/", response_model=UserCreate)(self.create_user)
        self.router.get("/users/me/", response_model=UserCreate)(self.me)

    def authenticate(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = self.auth_service.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self.auth_service.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def create_user(self, user: UserCreate):
        return self.auth_service.create_user(user)

    def me(self, token: str = Depends(AuthService.oauth2_scheme)):
        return self.auth_service.get_current_user(token)

# Dependency Injection function
def get_auth_service(user_repo: UserRepository = Depends()) -> AuthService:
    return AuthService(user_repo)