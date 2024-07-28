# qna_api/auth/controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from qna_api.auth.models import Token
from qna_api.auth.service import AuthService
from qna_api.core.logging import get_logger
from datetime import timedelta
from qna_api.core.config import settings

logger = get_logger(__name__)

class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/token", response_model=Token)(self.authenticate)

    async def authenticate(self, form_data: OAuth2PasswordRequestForm = Depends()):
        logger.info(f"Logging in user: {form_data.username}")
        user = self.auth_service.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self.auth_service.create_access_token(
                                    data={"sub": user.username,"roles": user.roles},
                                    expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
