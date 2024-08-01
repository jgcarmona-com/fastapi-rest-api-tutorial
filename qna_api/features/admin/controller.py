from fastapi import APIRouter, Depends, HTTPException, status
from mediatr import Mediator
from qna_api.crosscutting.authorization import get_admin_user
from qna_api.features.admin.commands.delete_user_command import DeleteUserCommand
from qna_api.features.user.models import User
from qna_api.features.admin.commands.enable_user_command import EnableUserCommand
from qna_api.features.admin.queries.get_all_users_query import GetAllUsersQuery
from qna_api.crosscutting.logging import get_logger
from qna_api.features.user.models import User

logger = get_logger(__name__)

class AdminController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter()
        self.router = APIRouter(dependencies=[Depends(get_admin_user)])
        self._add_routes()

    def _add_routes(self):
        self.router.get("/users", response_model=list[User])(self.get_all_users)
        self.router.put("/users/{user_id}/enable", response_model=User)(self.enable_user)    
        self.router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)(self.delete_user)

    async def get_all_users(self):
        logger.info(f"an admin user is retrieving all users")
        try:
            users = await self.mediator.send_async(GetAllUsersQuery())
            return users
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def enable_user(self, user_id: int):
        logger.info(f"an admin user is retrieving all users")
        try:
            enabled_user = await self.mediator.send_async(EnableUserCommand(user_id))
            return enabled_user
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))    

    async def delete_user(self, user_id: int):
        logger.info(f"An admin user is deleting user with id {user_id}")
        try:
            await self.mediator.send_async(DeleteUserCommand(user_id))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
