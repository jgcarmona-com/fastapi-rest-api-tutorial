from fastapi import APIRouter, Depends
from qna_api.auth.models import UserCreate
from qna_api.auth.service import AuthService

class UserController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/users/me/", response_model=UserCreate)(self.me)    

    def me(self, token: str = Depends(AuthService.oauth2_scheme)):
        return self.auth_service.get_current_user(token)
