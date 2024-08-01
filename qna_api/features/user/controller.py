from fastapi import APIRouter, Depends, HTTPException, status
from mediatr import Mediator
from qna_api.crosscutting.authorization import get_authenticated_user
from qna_api.features.user.commands.signup_command import SignupCommand
from qna_api.features.user.commands.update_user_command import UpdateUserCommand
from qna_api.features.user.commands.validate_user_command import ValidateUserCommand
from qna_api.features.user.models import User, SignupModel, UserUpdate
from qna_api.features.user.constants import (
    SIGNUP_DESCRIPTION,
    ME_DESCRIPTION,
    UPDATE_USER_DESCRIPTION,
    VALIDATE_USER_DESCRIPTION
)

class UserController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/signup", response_model=User, description=SIGNUP_DESCRIPTION)(self.signup)
        self.router.get("/me", response_model=User, description=ME_DESCRIPTION )(self.me)
        self.router.put("/{user_to_update_id}", response_model=User, description=UPDATE_USER_DESCRIPTION)(self.update_user)
        self.router.get("/validate", response_model=User, description=VALIDATE_USER_DESCRIPTION)(self.validate_user)

    async def signup(self, user: SignupModel):        
        try:
            created_user_entity = await self.mediator.send_async(SignupCommand(user))
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
    
    async def validate_user(self, token: str):
        try:
            validated_user_entity = await self.mediator.send_async(ValidateUserCommand(token))
            return User.model_validate(validated_user_entity, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))