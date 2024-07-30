from mediatr import Mediator
from qna_api.auth.auth_service import AuthService
from qna_api.core.logging import get_logger
from qna_api.domain.role import Role
from qna_api.domain.user import UserEntity
from qna_api.user.models import UserUpdate
from qna_api.user.repository import UserRepository

logger = get_logger(__name__)

class UpdateUserCommand():    
    def __init__(self, current_user_id:str, user_to_update_id:str, user_updates: UserUpdate):
        self.current_user_id = current_user_id
        self.user_to_update_id = user_to_update_id
        self.user_updates = user_updates

@Mediator.handler
class UpdateUserCommandHandler():
    def __init__(self):
        self.user_repository = UserRepository.instance()

    def handle(self, request: UpdateUserCommand) -> UserEntity:     
        logger.info(f"Updating user: {request.user_to_update_id}")
        current_user = self.user_repository.get(request.current_user_id)        

        if not current_user:
            logger.error("Current user not found")
            raise ValueError("Current user not found")
        if request.user_to_update_id != current_user.id and 'admin' not in [role.value for role in current_user.get_roles()]:
            logger.error("Not authorized to update this user")
            raise ValueError("Not authorized to update this user")
        
        user_to_update = self.user_repository.get(request.user_to_update_id)
        if not user_to_update:
            logger.error("User to update not found")
            raise ValueError("User to update not found")

        if request.user_updates.username and request.user_updates.username != user_to_update.username:
            user_to_update.username = request.user_updates.username
        if request.user_updates.email and request.user_updates.email != user_to_update.email:
            user_to_update.email = request.user_updates.email
        if request.user_updates.full_name and request.user_updates.full_name != user_to_update.full_name:
            user_to_update.full_name = request.user_updates.full_name
        if request.user_updates.disabled is not None and request.user_updates.disabled != user_to_update.disabled:
            user_to_update.disabled = request.user_updates.disabled
        if request.user_updates.password:
            new_hashed_password = AuthService.get_password_hash(request.user_updates.password)
            if new_hashed_password != user_to_update.hashed_password:
                user_to_update.hashed_password = new_hashed_password

        try:
            return self.user_repository.update(user_to_update)
        except ValueError as e:
            logger.error(f"Error updating user: {str(e)}")
            raise ValueError(f"Error updating user: {str(e)}")