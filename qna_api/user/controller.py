from fastapi import APIRouter, Depends, HTTPException, status
from qna_api.auth.authorization import get_authenticated_user
from qna_api.user.models import User, UserCreate, UserUpdate
from qna_api.user.service import UserService

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("", response_model=UserCreate)(self.create_user)
        self.router.get("/me", response_model=User)(self.me)
        self.router.put("/{user_id}", response_model=User)(self.update_user)

    async def create_user(self, user: UserCreate):
        return self.user_service.create_user(user)
    
    async def me(self, current_user: User = Depends(get_authenticated_user)):
        return current_user
    
    async def update_user(self, user_id: int, user_update: UserUpdate, current_user: User = Depends(get_authenticated_user)):
        updated_user = self.user_service.update_user(user_id, user_update, current_user)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this user or user not found",
            )
        return updated_user