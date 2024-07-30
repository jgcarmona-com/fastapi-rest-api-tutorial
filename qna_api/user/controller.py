from fastapi import APIRouter, Depends, HTTPException, status
from mediatr import Mediator
from qna_api.auth.authorization import get_authenticated_user
from qna_api.user.commands.create_user_command import CreateUserCommand
from qna_api.user.commands.update_user_command import UpdateUserCommand
from qna_api.user.models import User, UserCreate, UserUpdate

class UserController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("", response_model=User)(self.create_user)
        self.router.get("/me", response_model=User)(self.me)
        self.router.put("/{user_to_update_id}", response_model=User)(self.update_user)

    async def create_user(self, user: UserCreate):        
        try:
            created_user_entity = await self.mediator.send_async(CreateUserCommand(user))
            return User.model_validate(created_user_entity, from_attributes=True) 
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    async def me(self, current_user: User = Depends(get_authenticated_user)):
        return current_user
    
    async def update_user(self, user_to_update_id: int, user_update: UserUpdate, current_user: User = Depends(get_authenticated_user)):
        try:
            updated_user_entity = await self.mediator.send_async(UpdateUserCommand(current_user.id, user_to_update_id,  user_update))
            return User.model_validate(updated_user_entity, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))